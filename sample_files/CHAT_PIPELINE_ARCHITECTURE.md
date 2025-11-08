# Chat Pipeline Architecture

Visual diagrams of the chat interface pipeline architecture and data flow.

**Created:** 2025-11-08

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                     (Terminal + Readline)                       │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ User Input
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ChatController                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Processing Pipeline                     │  │
│  │  1. Validate Input                                        │  │
│  │  2. Store User Message                                    │  │
│  │  3. Retrieve Conversation History                         │  │
│  │  4. [Optional] RAG Context Augmentation                   │  │
│  │  5. Generate LLM Response                                 │  │
│  │  6. Store Assistant Response                              │  │
│  │  7. Return Response                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└───┬──────────────────┬──────────────────┬──────────────────┬───┘
    │                  │                  │                  │
    │                  │                  │                  │
    ▼                  ▼                  ▼                  ▼
┌─────────┐    ┌──────────────┐   ┌───────────┐    ┌──────────┐
│ OpenAI  │    │Conversation  │   │  Context  │    │ History  │
│   API   │    │  Manager     │   │ Augmentor │    │   File   │
│         │    │              │   │   (RAG)   │    │          │
└─────────┘    └──────┬───────┘   └─────┬─────┘    └──────────┘
                      │                  │
                      │                  │
                      ▼                  ▼
              ┌──────────────────────────────┐
              │         ChromaDB             │
              │  ┌────────────────────────┐  │
              │  │ conversations          │  │
              │  │ documentation          │  │
              │  │ (other collections)    │  │
              │  └────────────────────────┘  │
              └──────────────────────────────┘
```

---

## Detailed Data Flow Diagram

```
USER INPUT
    │
    ├──── Command (/help, /quit, etc.)
    │         │
    │         └──> handle_command() ──> Execute & Return
    │
    └──── Message
          │
          ▼
    ┌─────────────────────────────────────┐
    │  ChatController.process_user_input  │
    └─────────────────────────────────────┘
          │
          ├─> [1] Validate Input
          │       │
          │       └─> Return "" if empty
          │
          ├─> [2] Store User Message
          │       │
          │       └─> ConversationManager.add_message(role="user")
          │              │
          │              └─> ChromaDB.conversations.add()
          │
          ├─> [3] Retrieve Conversation History
          │       │
          │       ├─> Get system prompt
          │       ├─> Get conversation messages (up to max_history)
          │       └─> Build messages list [system, user1, assistant1, ...]
          │
          ├─> [4] RAG Context Augmentation (if enabled)
          │       │
          │       ├─> ContextAugmentor.retrieve_context(query)
          │       │      │
          │       │      └─> ChromaDB.documentation.query()
          │       │             │
          │       │             └─> Returns top N relevant chunks
          │       │
          │       ├─> Build augmented system prompt
          │       │      │
          │       │      └─> Inject documentation context
          │       │
          │       └─> Update messages[0] with augmented prompt
          │
          ├─> [Track] Save debug information
          │       │
          │       ├─> last_user_prompt = user_input
          │       ├─> last_system_prompt = messages[0]['content']
          │       ├─> last_context = messages.copy()
          │       └─> last_rag_sources = context_info
          │
          ├─> [5] Generate LLM Response
          │       │
          │       └─> OpenAI.chat.completions.create(messages)
          │              │
          │              └─> Returns assistant response text
          │
          ├─> [6] Store Assistant Response
          │       │
          │       └─> ConversationManager.add_message(role="assistant")
          │              │
          │              └─> ChromaDB.conversations.add()
          │
          └─> [7] Return Response
                  │
                  └─> Display to user
```

---

## Component Interaction Diagram

```
┌───────────────────────────────────────────────────────────────────┐
│                        Terminal Session                           │
│                                                                   │
│  startup:  setup_readline()                                      │
│            └─> Load ~/.memorydev/chat_history.txt                │
│                                                                   │
│  runtime:  User types message                                    │
│            └─> Readline provides history navigation              │
│                                                                   │
│  exit:     save_readline_history()                               │
│            └─> Save ~/.memorydev/chat_history.txt                │
│                                                                   │
└────────┬──────────────────────────────────────────────────────────┘
         │
         ▼
┌───────────────────────────────────────────────────────────────────┐
│                         ChatController                            │
│                                                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Config    │  │   Current    │  │    Debug     │           │
│  │             │  │ Conversation │  │   Tracking   │           │
│  │ • model     │  │              │  │              │           │
│  │ • temp      │  │ • conv_id    │  │ • last_user  │           │
│  │ • use_rag   │  │ • messages   │  │ • last_sys   │           │
│  │ • max_hist  │  │              │  │ • last_ctx   │           │
│  └─────────────┘  └──────────────┘  └──────────────┘           │
│                                                                   │
└───┬───────────────────────┬───────────────────────┬──────────────┘
    │                       │                       │
    │                       │                       │
    ▼                       ▼                       ▼
┌────────────┐      ┌──────────────┐      ┌──────────────┐
│  OpenAI    │      │Conversation  │      │   Context    │
│            │      │   Manager    │      │  Augmentor   │
│ • GPT-4    │      │              │      │              │
│ • GPT-4o   │      │ • start()    │      │ • retrieve() │
│ • mini     │      │ • add_msg()  │      │ • augment()  │
│            │      │ • get_conv() │      │              │
└────────────┘      └──────┬───────┘      └──────┬───────┘
                           │                     │
                           └──────┬──────────────┘
                                  │
                                  ▼
                          ┌──────────────┐
                          │   ChromaDB   │
                          │              │
                          │ Collections: │
                          │ • conversations (messages)
                          │ • documentation (RAG)
                          │ • facts_knowledge
                          │ • code_repository
                          └──────────────┘
```

---

## RAG Augmentation Flow

```
User Query: "How do I use ChromaDB embeddings?"
    │
    ▼
┌─────────────────────────────────────────┐
│  IF use_rag == True                     │
└─────────────────────────────────────────┘
    │
    ├─> ContextAugmentor.retrieve_context()
    │       │
    │       └─> Semantic Search
    │           ┌──────────────────────────────────────┐
    │           │ ChromaDB.documentation.query(        │
    │           │   query_texts=[user_input],          │
    │           │   n_results=rag_n_results            │
    │           │ )                                    │
    │           └──────────────────────────────────────┘
    │                  │
    │                  ▼
    │           ┌──────────────────────────────────────┐
    │           │ Returns: Top N documentation chunks  │
    │           │                                      │
    │           │ [                                    │
    │           │   {                                  │
    │           │     content: "...",                  │
    │           │     metadata: {                      │
    │           │       project: "...",                │
    │           │       file: "...",                   │
    │           │       ...                            │
    │           │     }                                │
    │           │   },                                 │
    │           │   ...                                │
    │           │ ]                                    │
    │           └──────────────────────────────────────┘
    │                  │
    │                  ▼
    └─> Build Augmented System Prompt
            │
            ▼
    ┌──────────────────────────────────────────────┐
    │ Original System Prompt:                      │
    │ "You are a helpful AI assistant..."         │
    │                                              │
    │ ## Relevant Documentation:                  │
    │ [1] project/file.md:                        │
    │ <chunk 1 content preview>...                │
    │                                              │
    │ [2] project/file2.md:                       │
    │ <chunk 2 content preview>...                │
    │                                              │
    │ Use this documentation to provide           │
    │ accurate, well-informed responses.          │
    └──────────────────────────────────────────────┘
            │
            ▼
    Send to OpenAI LLM with augmented context
```

---

## Message Storage Schema

```
User Message Storage:
┌─────────────────────────────────────────────────────────┐
│ ChromaDB Document                                       │
├─────────────────────────────────────────────────────────┤
│ id: "conv_20251108_190052_386b23_msg_0"               │
│ document: "What is ChromaDB?"                          │
│ metadata: {                                            │
│   conversation_id: "conv_20251108_190052_386b23"      │
│   message_id: "conv_20251108_190052_386b23_msg_0"     │
│   role: "user"                                         │
│   message_index: 0                                     │
│   timestamp: "2025-11-08T19:00:52.123456+00:00"       │
│   namespace: "conversations::conv_..."                 │
│   content_hash: "a3f5..."                              │
│   type: "conversation_message"                         │
│ }                                                      │
│ embedding: [0.123, -0.456, ...]  (1536 dimensions)    │
└─────────────────────────────────────────────────────────┘

Assistant Message Storage:
┌─────────────────────────────────────────────────────────┐
│ ChromaDB Document                                       │
├─────────────────────────────────────────────────────────┤
│ id: "conv_20251108_190052_386b23_msg_1"               │
│ document: "ChromaDB is an open-source vector..."       │
│ metadata: {                                            │
│   conversation_id: "conv_20251108_190052_386b23"      │
│   message_id: "conv_20251108_190052_386b23_msg_1"     │
│   role: "assistant"                                    │
│   message_index: 1                                     │
│   timestamp: "2025-11-08T19:00:56.789012+00:00"       │
│   model: "gpt-4o-mini"                                 │
│   temperature: 0.7                                     │
│   rag_used: false                                      │
│ }                                                      │
│ embedding: [0.789, -0.321, ...]                        │
└─────────────────────────────────────────────────────────┘
```

---

## /lastprompts Debug Flow

```
User types: /lastprompts
    │
    ▼
┌────────────────────────────────────────┐
│  print_options(controller)             │
└────────────────────────────────────────┘
    │
    ├─> Access controller.last_user_prompt
    │   └─> Display: "How do I use ChromaDB?"
    │
    ├─> Access controller.last_system_prompt
    │   └─> Display: Full system prompt (with RAG if enabled)
    │
    ├─> Access controller.last_rag_sources
    │   │
    │   ├─> IF RAG was used:
    │   │   └─> Display each documentation chunk:
    │   │       • Source: project/file.md
    │   │       • Content preview (200 chars)
    │   │
    │   └─> ELSE:
    │       └─> Display: "RAG not used in last iteration"
    │
    └─> Access controller.last_context
        └─> Display message breakdown:
            [0] system    - "You are a helpful AI..."
            [1] user      - "Previous message"
            [2] assistant - "Previous response"
            [3] user      - "Current message"
```

---

## History Persistence Flow

```
Session Start:
┌────────────────────────────────────────┐
│  setup_readline()                      │
└────────────────────────────────────────┘
    │
    ├─> Check if ~/.memorydev/chat_history.txt exists
    │
    ├─> IF exists:
    │   └─> readline.read_history_file()
    │       └─> Loads up to 1000 previous commands
    │
    └─> Configure readline:
        ├─> Set history length (1000)
        ├─> Set editing mode (emacs)
        └─> Enable tab completion

During Session:
    User types ↑  → Previous command from history
    User types ↓  → Next command from history
    User types text → New command added to memory

Session End:
┌────────────────────────────────────────┐
│  save_readline_history()               │
└────────────────────────────────────────┘
    │
    └─> readline.write_history_file()
        └─> Saves all commands to ~/.memorydev/chat_history.txt
            (up to 1000 most recent)

Next Session:
    Cycle repeats → Previous history available
```

---

## Context Window Management

```
Conversation has 30 messages (exceeds max_history=20)

_get_conversation_history():
    │
    ├─> Get system prompt
    │   messages = [{"role": "system", "content": "..."}]
    │
    ├─> Get all conversation messages from ChromaDB
    │   conv_messages = [msg_0, msg_1, ..., msg_29]  (30 messages)
    │
    ├─> Check if exceeds limit
    │   if len(conv_messages) > max_history:
    │
    └─> Take most recent messages only
        conv_messages = conv_messages[-20:]  (last 20 messages)

Final context sent to LLM:
┌──────────────────────────────────────┐
│ [0] system: "You are a helpful..."  │
│ [1] user: (message 11)               │
│ [2] assistant: (response 11)         │
│ [3] user: (message 12)               │
│ ...                                  │
│ [20] user: (latest message)          │
└──────────────────────────────────────┘
    │
    └─> Sent to OpenAI API
```

---

## Error Handling Flow

```
process_user_input():
    │
    ├─> [1] Validate Input
    │   └─> IF empty: return ""
    │
    ├─> [2-4] Store & Retrieve
    │   └─> (No expected errors - DB operations)
    │
    ├─> [5] Generate LLM Response
    │   │
    │   └─> TRY:
    │       └─> OpenAI API call
    │
    │       EXCEPT:
    │       ├─> API Error (rate limit, invalid key, etc.)
    │       ├─> Network Error
    │       └─> Other exceptions
    │           │
    │           └─> Return error message to user
    │               "Error generating response: <details>"
    │
    └─> [6] Store Assistant Response
        └─> (Continues even if error occurred)
```

---

## Complete Pipeline Summary

```
┌─────────────┐
│    USER     │
│   INPUT     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐      ┌──────────────┐
│   Validate &     │      │   Readline   │
│   Store Message  │◄─────│   History    │
└──────┬───────────┘      └──────────────┘
       │
       ▼
┌──────────────────┐
│   Retrieve       │      ┌──────────────┐
│   Conversation   │─────►│   ChromaDB   │
│   History        │      │conversations │
└──────┬───────────┘      └──────────────┘
       │
       ▼
┌──────────────────┐
│   RAG Context    │      ┌──────────────┐
│   (Optional)     │─────►│   ChromaDB   │
│   Augmentation   │      │documentation │
└──────┬───────────┘      └──────────────┘
       │
       ▼
┌──────────────────┐
│   Track Debug    │
│   Information    │
│   (lastprompts)  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   Generate LLM   │      ┌──────────────┐
│   Response       │─────►│   OpenAI     │
│                  │      │   API        │
└──────┬───────────┘      └──────────────┘
       │
       ▼
┌──────────────────┐
│   Store          │      ┌──────────────┐
│   Response       │─────►│   ChromaDB   │
│                  │      │conversations │
└──────┬───────────┘      └──────────────┘
       │
       ▼
┌──────────────────┐
│   Return to      │
│   User           │
└──────────────────┘
```

---

## Key Design Patterns

### 1. Pipeline Pattern
- Linear flow with clear stages
- Each stage has single responsibility
- Optional stages (RAG) can be toggled

### 2. Persistence Layer
- ChromaDB for structured conversational data
- File system for readline history
- Separation of concerns

### 3. Augmentation Pattern
- RAG as optional enhancement
- Non-intrusive to main flow
- Can be toggled runtime

### 4. Debug/Inspect Pattern
- Separate tracking of pipeline state
- Non-intrusive to main flow
- Accessible via command

### 5. Stateful Controller
- Maintains conversation context
- Tracks debug information
- Manages configurations
