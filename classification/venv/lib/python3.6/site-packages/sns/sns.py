import json
import boto
import cherrypy
from boto import utils, ec2


# Usage:
# from sns.sns import Pub
# cherrypy.tools.pub = Pub(<arn>)
# Then decorate functions you wish to authenticate:
# @cherrypy.tools.pub()


class Pub(cherrypy.Tool):
    def __init__(self, arn):
        self.arn = arn
        self.messages = []
        self.sns = boto.connect_sns()
        self.env, self.instance_id, self.instance_type = Pub.get_ec2_info()

        cherrypy.Tool.__init__(self, 'on_end_request',
                               self.publish,
                               priority=100)

    def append_msg(self, message):
        self.messages.append(message)

    def publish(self):
        if cherrypy.response.status == '200 OK':
            for msg in self.messages:
                msg.message['properties'].update({"task_domain": self.env,
                                                  "instance_id": self.instance_id,
                                                  "instance_size": self.instance_type})
                self.sns.publish(self.arn, json.dumps(msg.message), msg.subject)
        else:
            return

    def get_all_topics(self):
        return self.sns.get_all_subscriptions_by_topic(self.arn)

    @staticmethod
    def get_ec2_info():
        """
        Get env of ec2 box
        :return: None or prefix
        """

        try:
            instance_metadata = utils.get_instance_metadata(timeout=0.5, num_retries=1)
            region = instance_metadata['placement']['availability-zone'][:-1]
            instance_id = instance_metadata['instance-id']
            instance_type = instance_metadata['instance-type']
            conn = ec2.connect_to_region(region)
            tags = conn.get_all_tags(filters={'resource-id': instance_id, 'key': 'Env'})
            if tags:
                # return env, instance ID, instance Type
                return tags[0].value, instance_id, instance_type
            else:
                return None, None, None

        except KeyError as e:
            print 'Failed to get EC2 instance information: {_reason}'.format(_reason=e.message)
            return "test1", "test2", "test3"


class BaseSNS(object):
    def __init__(self, subject):
        self.subject = subject
        self.message = {
            "properties": {}
        }

    @property
    def user_id(self):
        return self.message['user_id']

    @user_id.setter
    def user_id(self, user_id):
        self.message['user_id'] = user_id

    @property
    def account_id(self):
        return self.message['account_id']

    @account_id.setter
    def account_id(self, account_id):
        self.message["account_id"] = account_id

    @property
    def event_type(self):
        return self.message['event_type']

    @event_type.setter
    def event_type(self, event_type):
        self.message["event_type"] = event_type

    @property
    def source(self):
        return self.message['source']

    @source.setter
    def source(self, source):
        self.message['source'] = source


class WorkflowEventMsg(BaseSNS):
    def __init__(self):
        super(WorkflowEventMsg, self).__init__("Workflow Events")

    @property
    def workflow_id(self):
        return self.message['properties']['workflow_id']

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        self.message['properties']["workflow_id"] = workflow_id

    @property
    def workflow_name(self):
        return self.message['properties']['workflow_name']

    @workflow_name.setter
    def workflow_name(self, workflow_name):
        self.message['properties']["workflow_name"] = workflow_name


class TaskEventMsg(WorkflowEventMsg):
    def __init__(self, **kwargs):
        super(TaskEventMsg, self).__init__()
        self.user_id = kwargs.get('user_id', None)
        self.account_id = kwargs.get('account_id', None)
        self.event_type = kwargs.get('event_type', None)
        self.source = kwargs.get('source', None)
        self.task_id = kwargs.get('task_id', None)
        self.task_name = kwargs.get('task_name', None)
        self.task_type = kwargs.get('task_type', None)
        self.workflow_id = kwargs.get('workflow_id', None)
        self.workflow_name = kwargs.get('workflow_name', None)

    @property
    def task_id(self):
        return self.message['properties']['task_id']

    @task_id.setter
    def task_id(self, task_id):
        self.message['properties']['task_id'] = task_id

    @property
    def task_name(self):
        return self.message['properties']['task_name']

    @task_name.setter
    def task_name(self, task_name):
        self.message['properties']["task_name"] = task_name

    @property
    def task_type(self):
        return self.message['properties']['task_type']

    @task_type.setter
    def task_type(self, task_type):
        self.message['properties']["task_type"] = task_type
