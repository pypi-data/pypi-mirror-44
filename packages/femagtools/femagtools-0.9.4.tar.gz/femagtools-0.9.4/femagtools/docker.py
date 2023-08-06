"""
    femagtools.docker
    ~~~~~~~~~~~~~~~~~

    Running FEMAG on Docker Swarm


"""
import os
import json
import logging
import threading
import femagtools.femag
import femagtools.job
try:
    from queue import Queue
except ImportError:
    from Queue import Queue  # python 2.7


logger = logging.getLogger(__name__)


def get_port_binding():
    """returns list with dict(HostIp, HostPort) of all
    running femag containers:
      [{'HostPort': '25555', 'HostIp': '0.0.0.0'}, 
       {'HostPort': '15555', 'HostIp': '0.0.0.0'}, 
       {'HostPort': '5555', 'HostIp': '0.0.0.0'}]
    """
    import docker
    client = docker.from_env()
    return [c.attrs['NetworkSettings']['Ports']['5555/tcp'][0]
            for c in client.containers.list(
                    filters={'label': 'org.label-schema.name=profemag/femag'})]


def publish_receive(message):
    """handle messages from femag publisher"""
    topic, content = message  # "femag_log" + text
    # topics: femag_log, progress, file_modified,
    #   model_image, calc_image, field_image, babs_image, demag_image, color_scale
    if topic == 'femag_log' or topic == 'progress':
        logger.info("%s: %s", topic, content.strip())
    else:
        logger.info('%s: len %d', topic, len(content.strip()))


class AsyncFemag(threading.Thread):
    def __init__(self, queue, workdir, port, host, stoponend):
        threading.Thread.__init__(self)
        self.queue = queue
        self.workdir = workdir
        self.stoponend = stoponend
        self.container = femagtools.femag.ZmqFemag(
            workdir,
            port, host)
        
    def run(self):
        """execute femag fsl task in task directory"""
        while True:
            task = self.queue.get()
            if task is None:
                break
            task.container = self.container  # used in get_results
            r = self.container.cleanup()
            for f in task.transfer_files:
                r = self.container.upload(os.path.join(task.directory, f))
            fslfile = os.path.join(task.directory, task.fsl_file)
            logger.info('Docker task %s %s',
                        task.id, task.fsl_file)
            fslcmds = []
            with open(fslfile) as f:
                fslcmds += f.readlines()
            ret = self.container.send_fsl(
                '\n'.join(fslcmds), publish_receive)[:2]
            logger.debug(ret)
            r = [json.loads(s)
                 for s in ret]
            logger.info("Finished %s", r)
            try:
                if r[0]['status'] == 'ok':
                    task.status = 'C'
                    status, content = self.container.getfile()[:2]  # last element is 'end.'
                    logging.info("get results %s: status %s len %d",
                                 task.id, status, len(content))
                    bchfile = json.loads(status)['message']
                    with open(os.path.join(task.directory,
                                           bchfile), 'wb') as f:
                        f.write(content)
                else:
                    task.status = 'X'
            except (KeyError, IndexError):
                task.status = 'X'

            if self.stoponend:
                self.container.quit()
                # lets hope that docker will always restart this container
            self.queue.task_done()
        
    
class Engine(object):

    """The Docker Engine

       execute Femag-Simulations with docker

       Args:
         hosts (list of str): list of container names
         stoponend (bool): stop container after each task (experimental)
    """
    def __init__(self, hosts=[], ports=[], stoponend=True):
        self.stoponend = stoponend
        if ports:
            self.femag_ports = ports
        else:
            self.femag_ports = [int(os.environ.get('FEMAG_PORT', 5555))]*len(hosts)
        if hosts:
            self.hosts = hosts
        else:
            self.hosts = ['127.0.0.1']*len(ports)
            
    def create_job(self, workdir):
        """Create a FEMAG :py:class:`CloudJob`

        Args:
            workdir (str): The workdir where the calculation files are stored

        Return:
            job (:class:`Job`)
        """
        if not self.hosts:
            raise ValueError("empty host list")
        self.queue = Queue()
        self.async_femags = [AsyncFemag(self.queue,
                                        workdir,
                                        p, h,
                                        self.stoponend)
                             for h, p in zip(self.hosts, self.femag_ports)]
        
        self.job = femagtools.job.Job(workdir)
        return self.job

    def submit(self):
        """Starts the FEMAG calculation(s) as Docker containers

        Return:
            number of started tasks (int)
        """
        
        for async_femag in self.async_femags:
            async_femag.start()

        for task in self.job.tasks:
            self.queue.put(task)

        return len(self.job.tasks)

    def join(self):
        """Wait until all calculations are finished

        Return:
            list of all calculations status (C = Ok, X = error) (:obj:`list`)
        """
        # block until all tasks are done
        self.queue.join()

        # stop workers
        for _ in self.async_femags:
            self.queue.put(None)
        for async_femag in self.async_femags:
            async_femag.join()
            
        return [t.status for t in self.job.tasks]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s')
    engine = Engine()
    job = engine.create_job('/tmp/tar/docker-femag')
    for _ in range(3):
        t = job.add_task()
        t.add_file('femag.fsl',
                   content=[''])
    engine.submit()
    status = engine.join()
    print("Status {}".format(status))
    for t in engine.job.tasks:
        print(t.directory)
    
