document.addEventListener('DOMContentLoaded', () => {
    const newNoteForm = document.getElementById('new-note-form');
    const userIdInput = document.getElementById('user-id');
    const noteContentInput = document.getElementById('note-content');
    const formMessage = document.getElementById('form-message');

    const fetchUserIdInput = document.getElementById('fetch-user-id');
    const fetchNotesButton = document.getElementById('fetch-notes-button');
    const notesList = document.getElementById('notes-list');
    const notesMessage = document.getElementById('notes-message');

    // Define the base URL for your API.
    // When running locally, your backend is likely at http://127.0.0.1:8000
    // This will need to change when deployed.
    const API_BASE_URL = 'http://127.0.0.1:8000'; 

    // --- Add New Note ---
    newNoteForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        const userId = userIdInput.value.trim();
        const content = noteContentInput.value.trim();

        if (!userId || !content) {
            formMessage.textContent = 'User ID and content are required.';
            formMessage.style.color = 'red';
            return;
        }

        formMessage.textContent = 'Adding note...';
        formMessage.style.color = 'blue';

        try {
            const response = await fetch(`${API_BASE_URL}/notes/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId, content: content }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Failed to add note. Server returned an error.' }));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const newNote = await response.json();
            formMessage.textContent = `Note added successfully! (ID: ${newNote.id})`;
            formMessage.style.color = 'green';
            noteContentInput.value = ''; // Clear content field
            
            // Optionally, refresh notes for the current user if the new note belongs to them
            if (userId === fetchUserIdInput.value.trim()) {
                fetchNotesForUser(userId);
            }

        } catch (error) {
            console.error('Error adding note:', error);
            formMessage.textContent = `Error: ${error.message}`;
            formMessage.style.color = 'red';
        }
    });

    // --- Fetch Notes ---
    fetchNotesButton.addEventListener('click', () => {
        const userIdToFetch = fetchUserIdInput.value.trim();
        if (!userIdToFetch) {
            notesMessage.textContent = 'Please enter a User ID to fetch notes.';
            notesMessage.style.color = 'red';
            notesList.innerHTML = ''; // Clear previous notes
            return;
        }
        fetchNotesForUser(userIdToFetch);
    });

    async function fetchNotesForUser(userId) {
        notesMessage.textContent = 'Fetching notes...';
        notesMessage.style.color = 'blue';
        notesList.innerHTML = ''; // Clear previous notes

        try {
            const response = await fetch(`${API_BASE_URL}/notes/user/${userId}`);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Failed to fetch notes. Server returned an error.' }));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const notes = await response.json();

            if (notes.length === 0) {
                notesMessage.textContent = 'No notes found for this user.';
                notesMessage.style.color = 'black';
            } else {
                notesMessage.textContent = `Displaying ${notes.length} note(s).`;
                notesMessage.style.color = 'green';
                notes.forEach(note => {
                    const listItem = document.createElement('li');
                    const createdDate = new Date(note.created_at).toLocaleString();
                    listItem.innerHTML = `
                        <strong>ID: ${note.id}</strong><br>
                        ${note.content}
                        <div class="note-meta">Created: ${createdDate}</div>
                    `;
                    notesList.appendChild(listItem);
                });
            }
        } catch (error) {
            console.error('Error fetching notes:', error);
            notesMessage.textContent = `Error: ${error.message}`;
            notesMessage.style.color = 'red';
        }
    }

    // Optionally, fetch notes for the default user ID on page load
    if (fetchUserIdInput.value.trim()) {
        fetchNotesForUser(fetchUserIdInput.value.trim());
    }
});