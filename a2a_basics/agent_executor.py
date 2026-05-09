##-----------------Imports-----------------
from a2a.utils.errors import InvalidRequestError
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.utils import new_task
from rich.pretty import pprint
from rich import print as cprint
import logging
import uuid
from a2a.types import (
    InternalError,
    Part,
    TextPart,
    TaskState,
    UnsupportedOperationError,
)
from a2a.utils.errors import ServerError
from WebSearchAgent import WebsearchAgent
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
class WebSearchAgentExecutor(AgentExecutor):
    """Websearch Remote Agent Implementation."""
    def __init__(self):
        self.agent = WebsearchAgent()
    
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # Checking if Context Exists ------------------------------------------
        pprint(context)
        if not context:
            print("no context found!")
            raise ServerError(error=InvalidRequestError())
        
        query = context.get_user_input()
        
        task = context.current_task

        if not task:
            task = new_task(context.message)  # type: ignore
            await event_queue.enqueue_event(task)
        # Creating the Task Updater for the Current Task (Task Id) and Context (Context Id)---------
        # - Which adds the Task Updates (Status or concrete Artifacts - responses) to the Event Queue
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        # Invoking the Agent with the received query -----------------------------
        try:
            # For Non-Streaming Implementation:
            #----------------------------------------------------------------
            result = self.agent.invoke(query, task.context_id)
            is_task_complete = result['is_task_complete']
            if is_task_complete:
                await updater.add_artifact(
                            [Part(root=TextPart(text=result['content']))],
                            name='websearch_result',)
                await updater.complete()
            # ---------------------------------------------------------------
        except Exception as e:
            logger.error(f'An error occurred while getting the response: {e}')
            raise
        
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise ServerError(error=UnsupportedOperationError())