# Copyright 2025 the LlamaFactory team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from enum import Enum, unique
from typing import Any, Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Literal


@unique
class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"
    TOOL = "tool"


@unique
class Finish(str, Enum):
    STOP = "stop"
    LENGTH = "length"
    TOOL = "tool_calls"


class ModelCard(BaseModel):
    id: str
    object: Literal["model"] = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: Literal["owner"] = "owner"


class ModelList(BaseModel):
    object: Literal["list"] = "list"
    data: list[ModelCard] = []


class Function(BaseModel):
    name: str
    arguments: str


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]


class FunctionAvailable(BaseModel):
    type: Literal["function", "code_interpreter"] = "function"
    function: Optional[FunctionDefinition] = None


class FunctionCall(BaseModel):
    id: str
    type: Literal["function"] = "function"
    function: Function


class URL(BaseModel):
    url: str
    detail: Literal["auto", "low", "high"] = "auto"


class MultimodalInputItem(BaseModel):
    type: Literal["text", "image_url", "video_url", "audio_url"]
    text: Optional[str] = None
    image_url: Optional[URL] = None
    video_url: Optional[URL] = None
    audio_url: Optional[URL] = None


class ChatMessage(BaseModel):
    role: Role
    content: Optional[Union[str, list[MultimodalInputItem]]] = None
    tool_calls: Optional[list[FunctionCall]] = None


class ChatCompletionMessage(BaseModel):
    role: Optional[Role] = None
    content: Optional[str] = None
    tool_calls: Optional[list[FunctionCall]] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    tools: Optional[list[FunctionAvailable]] = None
    do_sample: Optional[bool] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: int = 1
    max_tokens: Optional[int] = None
    stop: Optional[Union[str, list[str]]] = None
    stream: bool = False
    presence_penalty: Optional[float] = None
    repetition_penalty: Optional[float] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: Finish


class ChatCompletionStreamResponseChoice(BaseModel):
    index: int
    delta: ChatCompletionMessage
    finish_reason: Optional[Finish] = None


class ChatCompletionResponseUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: Literal["chat.completion"] = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: list[ChatCompletionResponseChoice]
    usage: ChatCompletionResponseUsage


class ChatCompletionStreamResponse(BaseModel):
    id: str
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: list[ChatCompletionStreamResponseChoice]


class ScoreEvaluationRequest(BaseModel):
    model: str
    messages: list[str]
    max_length: Optional[int] = None


class ScoreEvaluationResponse(BaseModel):
    id: str
    object: Literal["score.evaluation"] = "score.evaluation"
    model: str
    scores: list[float]
