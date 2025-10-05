# Django Messaging Application

This project is a Django-based messaging application that demonstrates the use of Django Signals, advanced ORM techniques, and caching strategies. It fulfills the requirements for the tasks in the `alx-backend-python` repository under the `Django-signals_orm-0x04` directory. The application allows users to send messages, receive notifications, view message edit history, manage threaded conversations, filter unread messages, and cache message views for performance.

## Features (Tasks)
1. **Task 0: Signals for User Notifications**
   - Automatically creates a `Notification` when a new `Message` is created using a `post_save` signal.
   - Models: `Message` and `Notification`.
   - Files: `messaging/models.py`, `messaging/signals.py`, `messaging/apps.py`, `messaging/admin.py`, `messaging/tests.py`.

2. **Task 1: Signal for Logging Message Edits**
   - Logs the old content of a message in a `MessageHistory` model before updates using a `pre_save` signal.
   - Displays edit history in a user interface.
   - Files: `messaging/models.py`, `messaging/signals.py`, `messaging/views.py`, `messaging/templates/messaging/message_history.html`.

3. **Task 2: Signals for Deleting User-Related Data**
   - Automatically cleans up messages, notifications, and message histories when a user deletes their account using a `post_delete` signal.
   - Includes a view to delete a user’s account.
   - Files: `messaging/views.py`, `messaging/signals.py`.

4. **Task 3: Advanced ORM Techniques for Threaded Conversations**
   - Implements threaded conversations with a self-referential `parent_message` field.
   - Uses `select_related` and `prefetch_related` to optimize queries for displaying message threads.
   - Files: `messaging/models.py`, `messaging/views.py`, `messaging/templates/messaging/conversation_thread.html`.

5. **Task 4: Custom ORM Manager for Unread Messages**
   - Provides a custom manager (`UnreadMessagesManager`) to filter unread messages for a user.
   - Optimizes queries with `.only()`.
   - Files: `messaging/models.py`, `messaging/views.py`, `messaging/templates/messaging/unread_messages.html`.

6. **Task 5: Basic View Cache**
   - Caches a view that lists messages for 60 seconds using `cache_page`.
   - Configures in-memory caching with `LocMemCache`.
   - Files: `messagingapp/settings.py`, `messaging/views.py`, `messaging/templates/messaging/message_list.html`.

## Repository Structure
- **Repository**: `alx-backend-python`
- **Directory**: `Django-signals_orm-0x04`
- **Files**:
  - `messaging/models.py`: Defines `Message`, `Notification`, and `MessageHistory` models.
  - `messaging/signals.py`: Contains signal handlers for notifications, edit logging, and user data cleanup.
  - `messaging/apps.py`: Configures signal imports.
  - `messaging/admin.py`: Registers models for admin interface.
  - `messaging/views.py`: Implements views for message history, user deletion, threaded conversations, unread messages, and cached message list.
  - `messaging/tests.py`: Contains unit tests for all tasks.
  - `messaging/templates/messaging/*.html`: Templates for message history, threaded conversations, unread messages, and message list.
  - `messagingapp/urls.py`: URL mappings for views.
  - `messagingapp/settings.py`: Configures caching and app settings.

## Prerequisites
- Python 3.8+
- Django 4.x
- Git

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/alx-backend-python.git
   cd alx-backend-python/Django-signals_orm-0x04
