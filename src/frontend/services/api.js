/**
 * API Service Layer
 * Handles all HTTP requests to the backend API
 */

const API_BASE_URL = 'http://localhost:5000/api/v1';

// Get JWT token from localStorage
function getToken() {
    return localStorage.getItem('token');
}

// Set JWT token in localStorage
function setToken(token) {
    localStorage.setItem('token', token);
}

// Remove JWT token from localStorage
function removeToken() {
    localStorage.removeItem('token');
}

// Get user info from localStorage
function getUserInfo() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Set user info in localStorage
function setUserInfo(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

// Remove user info from localStorage
function removeUserInfo() {
    localStorage.removeItem('user');
}

// Auth Service
const authService = {
    async register(email, password) {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Registration failed');
        }

        return data;
    },

    async login(email, password) {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Login failed');
        }

        // Store token and user info
        setToken(data.token);
        setUserInfo(data.user);

        return data;
    },

    logout() {
        removeToken();
        removeUserInfo();
    },

    isAuthenticated() {
        return !!getToken();
    }
};

// Task Service
const taskService = {
    async getTasks(page = 1, limit = 10) {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/tasks?page=${page}&limit=${limit}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch tasks');
        }

        return data;
    },

    async getTask(taskId) {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch task');
        }

        return data.task;
    },

    async createTask(taskData) {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(taskData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to create task');
        }

        return data.task;
    },

    async updateTask(taskId, taskData) {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(taskData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to update task');
        }

        return data.task;
    },

    async deleteTask(taskId) {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to delete task');
        }

        return data;
    }
};
