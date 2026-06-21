from nevara.utils.memory_utils import (
    messages_token_count, split_messages, summarizer,
    get_memory_dir, message_load_deserial,
)
from nevara.schema.types import messageList, MemoryConfig, messageType
from nevara.components.vector_db import HistoryDB
from nevara.prompts import load_prompt
import json

class PersistantLayer:
    def __init__(self):
        self.memory_dir = get_memory_dir()
        self.message_sav_path = self.memory_dir / "messages_sav.json"
        self.historyDB = HistoryDB(self.memory_dir, "history")
        
        self._loadMessages()
        
    def _loadMessages(self):
        if not self.message_sav_path.exists(): return
        self.messages = message_load_deserial(self.message_sav_path)
        
    def _saveMessages(self):
        with open(self.message_sav_path, 'w', encoding='utf-8') as f:
            message_serial = [msg.model_dump() for msg in self.messages]
            json.dump(message_serial, f, indent=4)
    
    def _retrieveRelatedHistory(self, query: str) -> list:
        return [document.page_content for document in self.historyDB.retrieve_doc(query)]
    
    def _serializeHistory(self, history: list[str]) -> str:
        return '\n'.join(
            self._formatIndexed(history)
        )
        
    def _formatIndexed(self, inList: list) -> list:
        return [
            f"{index}) {content}"
            for index, content in enumerate(inList, start=1)
        ]

class ConverstationMemoryBackend:
    def __init__(self) -> None:
        self.messages: messageList = []
        self.history: list[str] = []
    
    def _addMessages(self, message: messageType | messageList):
        if isinstance(message, messageType): message = [message]
        self.messages.extend(message)
    
    def _filterHistory(self, input_: list) -> list:
        return [
            doc
            for doc in input_
            if doc not in self.history
        ]
        
    def _clearMessage(self):
        self.messages.clear()
        
    def getMessages(self) -> messageList:
        return self.messages.copy()

class ConverstationMemory(
    PersistantLayer,
    ConverstationMemoryBackend,
):
    def __init__(self):
        super().__init__()
        self.max_messages_token = MemoryConfig.messages_ctx
        self.max_token_cap = MemoryConfig.messages_token_cap
        self.keep_latest_history = MemoryConfig.keepLatestHistory
        
    ### Elementary Methods (internal)
    def _isHistoryOverflow(self) -> bool:
        return len(self.history) > self.keep_latest_history
        
    def _isMessagesOverflow(self) -> bool:
        return messages_token_count(self.messages) <= int(self.max_messages_token * self.max_token_cap)
    
    def _maintainHistory(self, to_history: messageList):
        if self._isHistoryOverflow(): self.history = self.history[-self.keep_latest_history:]
        
        summary = self.historyDB.push_stamp_docs(summarizer(to_history))
        self.history.extend(summary)
    
    ### Compound Methods
    def build_history_prompt(self, query: str) -> str:
        retrieved_history = self._retrieveRelatedHistory(query)
        filtered_old_history = self._filterHistory(retrieved_history)
        
        return load_prompt(
            'memory/history',
            old_related_history=self._serializeHistory(filtered_old_history),
            ongoing_history=self._serializeHistory(self.history)
        )
    
    def maintainMessages(self) -> messageList:
        to_history, self.messages = split_messages(self.messages, self.max_messages_token)
        return to_history
    
    def maintainMemory(self):
        """
        maintainMemory does
        - check for overflow context, if yes then..
        - maintain what messages to keep, and rest to save into history bank.
        """
        if self._isMessagesOverflow(): return
        
        to_history = self.maintainMessages()
        self._maintainHistory(to_history)
        
    def commitMessage(self, message: messageType | messageList):
        self._addMessages(message)
        self._saveMessages()
        
    def session_end(self):
        """converts remaining messages to summary and saves into history db"""
        self._maintainHistory(self.messages)
        self._clearMessage()
        self._saveMessages()