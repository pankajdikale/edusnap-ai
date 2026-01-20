// src/services/api.ts
const BASE_URL = 'http://localhost:8000'; // Change if backend is on a different URL/port

// Helper to get auth token
const getAuthToken = (): string | null => {
  return localStorage.getItem('auth-token');
};

// Authenticated fetch helper
const authFetch = async (url: string, options: RequestInit = {}): Promise<any> => {
  const token = getAuthToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const response = await fetch(`${BASE_URL}${url}`, {
    ...options,
    headers: { ...headers, ...options.headers },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(errorData.detail || `HTTP ${response.status}`);
  }

  return response.json();
};

// Auth APIs
export const login = async (email: string, password: string) => {
  const response = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error('Invalid credentials');
  }

  const data = await response.json();
  localStorage.setItem('auth-token', data.token);
  return data;
};

export const logout = async () => {
  localStorage.removeItem('auth-token');
};

// Faculty Management
export const addFaculty = async (data: { username: string; name: string; email: string; department: string; year: string; password: string }) => {
  return authFetch('/api/admin/add-faculty', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const deleteFaculty = async (data: { email: string; password: string }) => {
  return authFetch('/api/admin/delete-faculty', {
    method: 'DELETE',
    body: JSON.stringify(data),
  });
};

// Student Management
export const addStudent = async (data: { name: string; rollNumber: string; department: string; semester: string; image: File | null }) => {
  const formData = new FormData();
  formData.append('name', data.name);
  formData.append('roll_no', data.rollNumber);
  formData.append('department', data.department);
  formData.append('semester', data.semester);
  if (data.image) formData.append('image', data.image);

  const token = getAuthToken();
  const headers: HeadersInit = {
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const response = await fetch(`${BASE_URL}/api/students/add`, {
    method: 'POST',
    headers,
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(errorData.detail || `HTTP ${response.status}`);
  }

  return response.json();
};

// Attendance
export const uploadAttendance = async (data: { image: File | null; department: string; year: string; course: string; subject: string }) => {
  const formData = new FormData();
  if (data.image) formData.append('file', data.image);
  formData.append('department', data.department);
  formData.append('year', data.year);
  formData.append('course', data.course);
  formData.append('subject', data.subject);

  const token = getAuthToken();
  console.log('Token being sent:', token);  // Debug log
  const headers: HeadersInit = {
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const response = await fetch(`${BASE_URL}/api/attendance/upload`, {
    method: 'POST',
    headers,
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
    console.error('Upload error:', errorData);  // Debug log
    throw new Error(errorData.detail || `HTTP ${response.status}`);
  }

  return response.json();
};

export const getAttendanceResults = async () => {
  return authFetch('/api/attendance/results');
};

// Reports
export const getAdminReports = async () => {
  return authFetch('/api/reports/admin');
};

export const getFacultyReports = async () => {
  return authFetch('/api/reports/faculty');
};