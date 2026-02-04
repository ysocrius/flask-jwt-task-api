/**
 * Main Application
 * Handles routing and UI rendering
 */

let currentPage = 'login';
let currentTaskPage = 1;
let editingTaskId = null;

// Router
function navigate(page) {
    currentPage = page;
    render();
}

// Main render function
function render() {
    const app = document.getElementById('app');

    // Check authentication for protected pages
    if (['dashboard', 'tasks'].includes(currentPage) && !authService.isAuthenticated()) {
        currentPage = 'login';
    }

    // Render appropriate page
    switch (currentPage) {
        case 'register':
            app.innerHTML = renderRegisterPage();
            attachRegisterHandlers();
            break;
        case 'login':
            app.innerHTML = renderLoginPage();
            attachLoginHandlers();
            break;
        case 'dashboard':
            app.innerHTML = renderDashboardPage();
            attachDashboardHandlers();
            loadTasks();
            break;
        default:
            app.innerHTML = renderLoginPage();
            attachLoginHandlers();
    }
}

// ===== REGISTER PAGE =====
function renderRegisterPage() {
    return `
        <div class="container">
            <h1>Create Account</h1>
            <p>Register for PrimeTrade Task Manager</p>
            
            <div id="message"></div>
            
            <form id="register-form">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required placeholder="you@example.com">
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required placeholder="Min 8 chars, uppercase, lowercase, number">
                </div>
                
                <div class="form-group">
                    <label for="confirm-password">Confirm Password</label>
                    <input type="password" id="confirm-password" name="confirm-password" required>
                </div>
                
                <button type="submit" class="btn btn-primary">Register</button>
            </form>
            
            <p style="margin-top: 20px;">
                Already have an account? <a href="#" class="link" onclick="navigate('login'); return false;">Login</a>
            </p>
        </div>
    `;
}

function attachRegisterHandlers() {
    const form = document.getElementById('register-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        // Client-side validation
        if (password !== confirmPassword) {
            showMessage('Passwords do not match', 'error');
            return;
        }

        try {
            await authService.register(email, password);
            showMessage('Registration successful! Please login.', 'success');
            setTimeout(() => navigate('login'), 2000);
        } catch (error) {
            showMessage(error.message, 'error');
        }
    });
}

// ===== LOGIN PAGE =====
function renderLoginPage() {
    return `
        <div class="container">
            <h1>Welcome Back</h1>
            <p>Login to PrimeTrade Task Manager</p>
            
            <div id="message"></div>
            
            <form id="login-form">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required placeholder="you@example.com">
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn btn-primary">Login</button>
            </form>
            
            <p style="margin-top: 20px;">
                Don't have an account? <a href="#" class="link" onclick="navigate('register'); return false;">Register</a>
            </p>
        </div>
    `;
}

function attachLoginHandlers() {
    const form = document.getElementById('login-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            await authService.login(email, password);
            showMessage('Login successful!', 'success');
            setTimeout(() => navigate('dashboard'), 1000);
        } catch (error) {
            showMessage(error.message, 'error');
        }
    });
}

// ===== DASHBOARD PAGE =====
function renderDashboardPage() {
    const user = getUserInfo();

    return `
        <div class="container">
            <div class="header">
                <div>
                    <h1>Task Manager</h1>
                    <div class="user-info">Logged in as: ${user.email} (${user.role})</div>
                </div>
                <button class="btn btn-secondary" onclick="handleLogout()">Logout</button>
            </div>
            
            <div id="message"></div>
            
            <div style="margin-bottom: 20px;">
                <button class="btn btn-success" onclick="showCreateTaskForm()">+ Create New Task</button>
            </div>
            
            <div id="task-form-container" class="hidden"></div>
            
            <div id="task-list-container">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading tasks...</p>
                </div>
            </div>
        </div>
    `;
}

function attachDashboardHandlers() {
    // Handlers are attached inline in the HTML
}

async function loadTasks(page = 1) {
    currentTaskPage = page;
    const container = document.getElementById('task-list-container');

    try {
        const data = await taskService.getTasks(page, 10);

        if (data.tasks.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📝</div>
                    <h2>No tasks yet</h2>
                    <p>Create your first task to get started!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="task-list">
                ${data.tasks.map(task => renderTaskItem(task)).join('')}
            </div>
            
            <div class="pagination">
                <button class="btn btn-secondary btn-small" 
                        onclick="loadTasks(${page - 1})" 
                        ${page === 1 ? 'disabled' : ''}>
                    Previous
                </button>
                
                <span class="pagination-info">
                    Page ${data.page} of ${data.total_pages} (${data.total} total)
                </span>
                
                <button class="btn btn-secondary btn-small" 
                        onclick="loadTasks(${page + 1})" 
                        ${page === data.total_pages ? 'disabled' : ''}>
                    Next
                </button>
            </div>
        `;
    } catch (error) {
        container.innerHTML = `
            <div class="message message-error">
                Failed to load tasks: ${error.message}
            </div>
        `;
    }
}

function renderTaskItem(task) {
    return `
        <div class="task-item">
            <div class="task-header">
                <div>
                    <div class="task-title">${escapeHtml(task.title)}</div>
                    <span class="task-status status-${task.status}">${task.status.replace('_', ' ')}</span>
                </div>
            </div>
            
            ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
            
            <div class="task-actions">
                <button class="btn btn-primary btn-small" onclick="showEditTaskForm(${task.id})">Edit</button>
                <button class="btn btn-danger btn-small" onclick="handleDeleteTask(${task.id})">Delete</button>
            </div>
            
            <div class="task-meta">
                Created: ${new Date(task.created_at).toLocaleString()}
            </div>
        </div>
    `;
}

// ===== TASK FORM =====
function showCreateTaskForm() {
    editingTaskId = null;
    const container = document.getElementById('task-form-container');
    container.classList.remove('hidden');
    container.innerHTML = renderTaskForm();
}

async function showEditTaskForm(taskId) {
    editingTaskId = taskId;
    const container = document.getElementById('task-form-container');

    try {
        const task = await taskService.getTask(taskId);
        container.classList.remove('hidden');
        container.innerHTML = renderTaskForm(task);
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

function renderTaskForm(task = null) {
    return `
        <div style="background: #f8f9fa; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
            <h2>${task ? 'Edit Task' : 'Create New Task'}</h2>
            
            <form id="task-form">
                <div class="form-group">
                    <label for="task-title">Title *</label>
                    <input type="text" id="task-title" required maxlength="200" 
                           value="${task ? escapeHtml(task.title) : ''}">
                </div>
                
                <div class="form-group">
                    <label for="task-description">Description</label>
                    <textarea id="task-description">${task ? escapeHtml(task.description || '') : ''}</textarea>
                </div>
                
                <div class="form-group">
                    <label for="task-status">Status</label>
                    <select id="task-status">
                        <option value="pending" ${task && task.status === 'pending' ? 'selected' : ''}>Pending</option>
                        <option value="in_progress" ${task && task.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                        <option value="completed" ${task && task.status === 'completed' ? 'selected' : ''}>Completed</option>
                    </select>
                </div>
                
                <div style="display: flex; gap: 12px;">
                    <button type="submit" class="btn btn-success">${task ? 'Update' : 'Create'} Task</button>
                    <button type="button" class="btn btn-secondary" onclick="hideTaskForm()">Cancel</button>
                </div>
            </form>
        </div>
    `;
}

function hideTaskForm() {
    const container = document.getElementById('task-form-container');
    container.classList.add('hidden');
    container.innerHTML = '';
    editingTaskId = null;
}

// Attach task form handler after rendering
document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('submit', async (e) => {
        if (e.target.id === 'task-form') {
            e.preventDefault();

            const title = document.getElementById('task-title').value;
            const description = document.getElementById('task-description').value;
            const status = document.getElementById('task-status').value;

            const taskData = { title, description, status };

            try {
                if (editingTaskId) {
                    await taskService.updateTask(editingTaskId, taskData);
                    showMessage('Task updated successfully!', 'success');
                } else {
                    await taskService.createTask(taskData);
                    showMessage('Task created successfully!', 'success');
                }

                hideTaskForm();
                loadTasks(currentTaskPage);
            } catch (error) {
                showMessage(error.message, 'error');
            }
        }
    });
});

// ===== HANDLERS =====
async function handleDeleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    try {
        await taskService.deleteTask(taskId);
        showMessage('Task deleted successfully!', 'success');
        loadTasks(currentTaskPage);
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

function handleLogout() {
    authService.logout();
    showMessage('Logged out successfully', 'success');
    setTimeout(() => navigate('login'), 1000);
}

// ===== UTILITIES =====
function showMessage(message, type = 'success') {
    const container = document.getElementById('message');
    if (!container) return;

    container.innerHTML = `
        <div class="message message-${type}">
            ${escapeHtml(message)}
        </div>
    `;

    // Auto-hide after 5 seconds
    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    render();
});
