# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.cloud.tasks_v2beta2.proto import (
    cloudtasks_pb2 as google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2,
)
from google.cloud.tasks_v2beta2.proto import (
    queue_pb2 as google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2,
)
from google.cloud.tasks_v2beta2.proto import (
    task_pb2 as google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2,
)
from google.iam.v1 import iam_policy_pb2 as google_dot_iam_dot_v1_dot_iam__policy__pb2
from google.iam.v1 import policy_pb2 as google_dot_iam_dot_v1_dot_policy__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class CloudTasksStub(object):
    """Cloud Tasks allows developers to manage the execution of background
  work in their applications.
  """

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.ListQueues = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/ListQueues",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ListQueuesRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ListQueuesResponse.FromString,
        )
        self.GetQueue = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/GetQueue",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.GetQueueRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.FromString,
        )
        self.CreateQueue = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/CreateQueue",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.CreateQueueRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.FromString,
        )
        self.UpdateQueue = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/UpdateQueue",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.UpdateQueueRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.FromString,
        )
        self.DeleteQueue = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/DeleteQueue",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.DeleteQueueRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.PurgeQueue = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/PurgeQueue",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.PurgeQueueRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.FromString,
        )
        self.PauseQueue = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/PauseQueue",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.PauseQueueRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.FromString,
        )
        self.ResumeQueue = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/ResumeQueue",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ResumeQueueRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.FromString,
        )
        self.GetIamPolicy = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/GetIamPolicy",
            request_serializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.GetIamPolicyRequest.SerializeToString,
            response_deserializer=google_dot_iam_dot_v1_dot_policy__pb2.Policy.FromString,
        )
        self.SetIamPolicy = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/SetIamPolicy",
            request_serializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.SetIamPolicyRequest.SerializeToString,
            response_deserializer=google_dot_iam_dot_v1_dot_policy__pb2.Policy.FromString,
        )
        self.TestIamPermissions = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/TestIamPermissions",
            request_serializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.TestIamPermissionsRequest.SerializeToString,
            response_deserializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.TestIamPermissionsResponse.FromString,
        )
        self.ListTasks = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/ListTasks",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ListTasksRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ListTasksResponse.FromString,
        )
        self.GetTask = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/GetTask",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.GetTaskRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.FromString,
        )
        self.CreateTask = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/CreateTask",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.CreateTaskRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.FromString,
        )
        self.DeleteTask = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/DeleteTask",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.DeleteTaskRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.LeaseTasks = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/LeaseTasks",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.LeaseTasksRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.LeaseTasksResponse.FromString,
        )
        self.AcknowledgeTask = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/AcknowledgeTask",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.AcknowledgeTaskRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.RenewLease = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/RenewLease",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.RenewLeaseRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.FromString,
        )
        self.CancelLease = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/CancelLease",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.CancelLeaseRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.FromString,
        )
        self.RunTask = channel.unary_unary(
            "/google.cloud.tasks.v2beta2.CloudTasks/RunTask",
            request_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.RunTaskRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.FromString,
        )


class CloudTasksServicer(object):
    """Cloud Tasks allows developers to manage the execution of background
  work in their applications.
  """

    def ListQueues(self, request, context):
        """Lists queues.

    Queues are returned in lexicographical order.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetQueue(self, request, context):
        """Gets a queue.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateQueue(self, request, context):
        """Creates a queue.

    Queues created with this method allow tasks to live for a maximum of 31
    days. After a task is 31 days old, the task will be deleted regardless of
    whether it was dispatched or not.

    WARNING: Using this method may have unintended side effects if you are
    using an App Engine `queue.yaml` or `queue.xml` file to manage your queues.
    Read
    [Overview of Queue Management and
    queue.yaml](https://cloud.google.com/tasks/docs/queue-yaml) before using
    this method.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateQueue(self, request, context):
        """Updates a queue.

    This method creates the queue if it does not exist and updates
    the queue if it does exist.

    Queues created with this method allow tasks to live for a maximum of 31
    days. After a task is 31 days old, the task will be deleted regardless of
    whether it was dispatched or not.

    WARNING: Using this method may have unintended side effects if you are
    using an App Engine `queue.yaml` or `queue.xml` file to manage your queues.
    Read
    [Overview of Queue Management and
    queue.yaml](https://cloud.google.com/tasks/docs/queue-yaml) before using
    this method.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteQueue(self, request, context):
        """Deletes a queue.

    This command will delete the queue even if it has tasks in it.

    Note: If you delete a queue, a queue with the same name can't be created
    for 7 days.

    WARNING: Using this method may have unintended side effects if you are
    using an App Engine `queue.yaml` or `queue.xml` file to manage your queues.
    Read
    [Overview of Queue Management and
    queue.yaml](https://cloud.google.com/tasks/docs/queue-yaml) before using
    this method.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def PurgeQueue(self, request, context):
        """Purges a queue by deleting all of its tasks.

    All tasks created before this method is called are permanently deleted.

    Purge operations can take up to one minute to take effect. Tasks
    might be dispatched before the purge takes effect. A purge is irreversible.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def PauseQueue(self, request, context):
        """Pauses the queue.

    If a queue is paused then the system will stop dispatching tasks
    until the queue is resumed via
    [ResumeQueue][google.cloud.tasks.v2beta2.CloudTasks.ResumeQueue]. Tasks can
    still be added when the queue is paused. A queue is paused if its
    [state][google.cloud.tasks.v2beta2.Queue.state] is
    [PAUSED][google.cloud.tasks.v2beta2.Queue.State.PAUSED].
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ResumeQueue(self, request, context):
        """Resume a queue.

    This method resumes a queue after it has been
    [PAUSED][google.cloud.tasks.v2beta2.Queue.State.PAUSED] or
    [DISABLED][google.cloud.tasks.v2beta2.Queue.State.DISABLED]. The state of a
    queue is stored in the queue's
    [state][google.cloud.tasks.v2beta2.Queue.state]; after calling this method
    it will be set to
    [RUNNING][google.cloud.tasks.v2beta2.Queue.State.RUNNING].

    WARNING: Resuming many high-QPS queues at the same time can
    lead to target overloading. If you are resuming high-QPS
    queues, follow the 500/50/5 pattern described in
    [Managing Cloud Tasks Scaling
    Risks](https://cloud.google.com/tasks/docs/manage-cloud-task-scaling).
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetIamPolicy(self, request, context):
        """Gets the access control policy for a
    [Queue][google.cloud.tasks.v2beta2.Queue]. Returns an empty policy if the
    resource exists and does not have a policy set.

    Authorization requires the following
    [Google IAM](https://cloud.google.com/iam) permission on the specified
    resource parent:

    * `cloudtasks.queues.getIamPolicy`
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def SetIamPolicy(self, request, context):
        """Sets the access control policy for a
    [Queue][google.cloud.tasks.v2beta2.Queue]. Replaces any existing policy.

    Note: The Cloud Console does not check queue-level IAM permissions yet.
    Project-level permissions are required to use the Cloud Console.

    Authorization requires the following
    [Google IAM](https://cloud.google.com/iam) permission on the specified
    resource parent:

    * `cloudtasks.queues.setIamPolicy`
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def TestIamPermissions(self, request, context):
        """Returns permissions that a caller has on a
    [Queue][google.cloud.tasks.v2beta2.Queue]. If the resource does not exist,
    this will return an empty set of permissions, not a
    [NOT_FOUND][google.rpc.Code.NOT_FOUND] error.

    Note: This operation is designed to be used for building permission-aware
    UIs and command-line tools, not for authorization checking. This operation
    may "fail open" without warning.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListTasks(self, request, context):
        """Lists the tasks in a queue.

    By default, only the [BASIC][google.cloud.tasks.v2beta2.Task.View.BASIC]
    view is retrieved due to performance considerations;
    [response_view][google.cloud.tasks.v2beta2.ListTasksRequest.response_view]
    controls the subset of information which is returned.

    The tasks may be returned in any order. The ordering may change at any
    time.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetTask(self, request, context):
        """Gets a task.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateTask(self, request, context):
        """Creates a task and adds it to a queue.

    Tasks cannot be updated after creation; there is no UpdateTask command.

    * For [App Engine queues][google.cloud.tasks.v2beta2.AppEngineHttpTarget],
    the maximum task size is
    100KB.
    * For [pull queues][google.cloud.tasks.v2beta2.PullTarget], the maximum
    task size is 1MB.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteTask(self, request, context):
        """Deletes a task.

    A task can be deleted if it is scheduled or dispatched. A task
    cannot be deleted if it has completed successfully or permanently
    failed.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def LeaseTasks(self, request, context):
        """Leases tasks from a pull queue for
    [lease_duration][google.cloud.tasks.v2beta2.LeaseTasksRequest.lease_duration].

    This method is invoked by the worker to obtain a lease. The
    worker must acknowledge the task via
    [AcknowledgeTask][google.cloud.tasks.v2beta2.CloudTasks.AcknowledgeTask]
    after they have performed the work associated with the task.

    The [payload][google.cloud.tasks.v2beta2.PullMessage.payload] is intended
    to store data that the worker needs to perform the work associated with the
    task. To return the payloads in the
    [response][google.cloud.tasks.v2beta2.LeaseTasksResponse], set
    [response_view][google.cloud.tasks.v2beta2.LeaseTasksRequest.response_view]
    to [FULL][google.cloud.tasks.v2beta2.Task.View.FULL].

    A maximum of 10 qps of
    [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks] requests are
    allowed per queue. [RESOURCE_EXHAUSTED][google.rpc.Code.RESOURCE_EXHAUSTED]
    is returned when this limit is
    exceeded. [RESOURCE_EXHAUSTED][google.rpc.Code.RESOURCE_EXHAUSTED]
    is also returned when
    [max_tasks_dispatched_per_second][google.cloud.tasks.v2beta2.RateLimits.max_tasks_dispatched_per_second]
    is exceeded.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def AcknowledgeTask(self, request, context):
        """Acknowledges a pull task.

    The worker, that is, the entity that
    [leased][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks] this task must
    call this method to indicate that the work associated with the task has
    finished.

    The worker must acknowledge a task within the
    [lease_duration][google.cloud.tasks.v2beta2.LeaseTasksRequest.lease_duration]
    or the lease will expire and the task will become available to be leased
    again. After the task is acknowledged, it will not be returned
    by a later [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks],
    [GetTask][google.cloud.tasks.v2beta2.CloudTasks.GetTask], or
    [ListTasks][google.cloud.tasks.v2beta2.CloudTasks.ListTasks].
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def RenewLease(self, request, context):
        """Renew the current lease of a pull task.

    The worker can use this method to extend the lease by a new
    duration, starting from now. The new task lease will be
    returned in the task's
    [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time].
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CancelLease(self, request, context):
        """Cancel a pull task's lease.

    The worker can use this method to cancel a task's lease by
    setting its [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time]
    to now. This will make the task available to be leased to the next caller
    of [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks].
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def RunTask(self, request, context):
        """Forces a task to run now.

    When this method is called, Cloud Tasks will dispatch the task, even if
    the task is already running, the queue has reached its
    [RateLimits][google.cloud.tasks.v2beta2.RateLimits] or is
    [PAUSED][google.cloud.tasks.v2beta2.Queue.State.PAUSED].

    This command is meant to be used for manual debugging. For
    example, [RunTask][google.cloud.tasks.v2beta2.CloudTasks.RunTask] can be
    used to retry a failed task after a fix has been made or to manually force
    a task to be dispatched now.

    The dispatched task is returned. That is, the task that is returned
    contains the [status][google.cloud.tasks.v2beta2.Task.status] after the
    task is dispatched but before the task is received by its target.

    If Cloud Tasks receives a successful response from the task's
    target, then the task will be deleted; otherwise the task's
    [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time] will be
    reset to the time that
    [RunTask][google.cloud.tasks.v2beta2.CloudTasks.RunTask] was called plus
    the retry delay specified in the queue's
    [RetryConfig][google.cloud.tasks.v2beta2.RetryConfig].

    [RunTask][google.cloud.tasks.v2beta2.CloudTasks.RunTask] returns
    [NOT_FOUND][google.rpc.Code.NOT_FOUND] when it is called on a
    task that has already succeeded or permanently failed.

    [RunTask][google.cloud.tasks.v2beta2.CloudTasks.RunTask] cannot be called
    on a [pull task][google.cloud.tasks.v2beta2.PullMessage].
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_CloudTasksServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ListQueues": grpc.unary_unary_rpc_method_handler(
            servicer.ListQueues,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ListQueuesRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ListQueuesResponse.SerializeToString,
        ),
        "GetQueue": grpc.unary_unary_rpc_method_handler(
            servicer.GetQueue,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.GetQueueRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.SerializeToString,
        ),
        "CreateQueue": grpc.unary_unary_rpc_method_handler(
            servicer.CreateQueue,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.CreateQueueRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.SerializeToString,
        ),
        "UpdateQueue": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateQueue,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.UpdateQueueRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.SerializeToString,
        ),
        "DeleteQueue": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteQueue,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.DeleteQueueRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "PurgeQueue": grpc.unary_unary_rpc_method_handler(
            servicer.PurgeQueue,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.PurgeQueueRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.SerializeToString,
        ),
        "PauseQueue": grpc.unary_unary_rpc_method_handler(
            servicer.PauseQueue,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.PauseQueueRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.SerializeToString,
        ),
        "ResumeQueue": grpc.unary_unary_rpc_method_handler(
            servicer.ResumeQueue,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ResumeQueueRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_queue__pb2.Queue.SerializeToString,
        ),
        "GetIamPolicy": grpc.unary_unary_rpc_method_handler(
            servicer.GetIamPolicy,
            request_deserializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.GetIamPolicyRequest.FromString,
            response_serializer=google_dot_iam_dot_v1_dot_policy__pb2.Policy.SerializeToString,
        ),
        "SetIamPolicy": grpc.unary_unary_rpc_method_handler(
            servicer.SetIamPolicy,
            request_deserializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.SetIamPolicyRequest.FromString,
            response_serializer=google_dot_iam_dot_v1_dot_policy__pb2.Policy.SerializeToString,
        ),
        "TestIamPermissions": grpc.unary_unary_rpc_method_handler(
            servicer.TestIamPermissions,
            request_deserializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.TestIamPermissionsRequest.FromString,
            response_serializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.TestIamPermissionsResponse.SerializeToString,
        ),
        "ListTasks": grpc.unary_unary_rpc_method_handler(
            servicer.ListTasks,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ListTasksRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.ListTasksResponse.SerializeToString,
        ),
        "GetTask": grpc.unary_unary_rpc_method_handler(
            servicer.GetTask,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.GetTaskRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.SerializeToString,
        ),
        "CreateTask": grpc.unary_unary_rpc_method_handler(
            servicer.CreateTask,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.CreateTaskRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.SerializeToString,
        ),
        "DeleteTask": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteTask,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.DeleteTaskRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "LeaseTasks": grpc.unary_unary_rpc_method_handler(
            servicer.LeaseTasks,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.LeaseTasksRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.LeaseTasksResponse.SerializeToString,
        ),
        "AcknowledgeTask": grpc.unary_unary_rpc_method_handler(
            servicer.AcknowledgeTask,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.AcknowledgeTaskRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "RenewLease": grpc.unary_unary_rpc_method_handler(
            servicer.RenewLease,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.RenewLeaseRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.SerializeToString,
        ),
        "CancelLease": grpc.unary_unary_rpc_method_handler(
            servicer.CancelLease,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.CancelLeaseRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.SerializeToString,
        ),
        "RunTask": grpc.unary_unary_rpc_method_handler(
            servicer.RunTask,
            request_deserializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_cloudtasks__pb2.RunTaskRequest.FromString,
            response_serializer=google_dot_cloud_dot_tasks__v2beta2_dot_proto_dot_task__pb2.Task.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "google.cloud.tasks.v2beta2.CloudTasks", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
