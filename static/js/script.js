// Main JavaScript for Schedule App with Multi-Select Support
class ScheduleApp {
    constructor() {
        this.state = {
            schools: [],
            groups: [],
            teachers: [],
            years: [],
            selectedFilters: {
                schoolIds: [], // Changed to arrays for multi-select
                groupIds: [],
                teacherIds: [],
                years: []
            },
            currentSchedule: null,
            isLoading: false
        };
        
        this.init();
    }
    
    async init() {
        await this.loadInitialData();
        this.bindEvents();
        this.updateUI();
    }
    
    async loadInitialData() {
        try {
            this.showLoading(true);
            
            // Load all initial data
            const [schools, years] = await Promise.all([
                this.fetchAPI('/api/schools'),
                this.fetchAPI('/api/years')
            ]);
            
            this.state.schools = schools;
            this.state.years = years;
            
            this.populateSelect('school-select', schools, 'id', 'name');
            this.populateSelect('year-select', years, null, null, true);
            
        } catch (error) {
            this.showError('Błąd ładowania danych: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    bindEvents() {
        // Filter selects
        document.getElementById('school-select').addEventListener('change', (e) => {
            this.onSchoolChange(e.target.value);
        });
        
        // Show schedule button
        document.getElementById('show-schedule-btn').addEventListener('click', () => {
            this.showSchedule();
        });
        
        // Back button
        document.getElementById('back-btn').addEventListener('click', () => {
            this.switchToFiltersView();
        });
        
        // Options button
        document.getElementById('options-btn').addEventListener('click', () => {
            this.toggleOptionsPanel();
        });
        
        // Apply filters button
        document.getElementById('apply-filters-btn').addEventListener('click', () => {
            this.applyFilters();
        });
        
        // Clear filters button
        document.getElementById('clear-filters-btn').addEventListener('click', () => {
            this.clearFilters();
        });
        
        // Close options panel when clicking outside
        document.addEventListener('click', (e) => {
            const optionsPanel = document.getElementById('options-panel');
            const optionsBtn = document.getElementById('options-btn');
            
            if (optionsPanel.style.display === 'block' && 
                !optionsPanel.contains(e.target) && 
                !optionsBtn.contains(e.target)) {
                this.toggleOptionsPanel(false);
            }
        });
    }
    
    async onSchoolChange(schoolId) {
        // Update single school selection for the simple select dropdown
        if (schoolId) {
            this.state.selectedFilters.schoolIds = [parseInt(schoolId)];
        } else {
            this.state.selectedFilters.schoolIds = [];
        }
        
        // Reset dependent filters
        this.state.selectedFilters.groupIds = [];
        this.state.selectedFilters.teacherIds = [];
        
        if (schoolId) {
            try {
                this.showLoading(true);
                
                const [groups, teachers] = await Promise.all([
                    this.fetchAPI(`/api/groups/${schoolId}`),
                    this.fetchAPI(`/api/teachers/${schoolId}`)
                ]);
                
                this.state.groups = groups;
                this.state.teachers = teachers;
                
                this.populateSelect('group-select', groups, 'id', 'name');
                this.populateSelect('teacher-select', teachers, 'id', null, false, (teacher) => 
                    `${teacher.name} ${teacher.surname}`);
                
                // Enable selects
                document.getElementById('group-select').disabled = false;
                document.getElementById('teacher-select').disabled = false;
                
            } catch (error) {
                this.showError('Błąd ładowania danych szkoły: ' + error.message);
            } finally {
                this.showLoading(false);
            }
        } else {
            // Clear and disable dependent selects
            this.clearSelect('group-select', 'Wszystkie klasy');
            this.clearSelect('teacher-select', 'Wszyscy nauczyciele');
            document.getElementById('group-select').disabled = true;
            document.getElementById('teacher-select').disabled = true;
        }
        
        this.updateUI();
    }
    
    async showSchedule() {
        try {
            this.showLoading(true);
            
            // Collect current filter values from simple selects
            const schoolId = document.getElementById('school-select').value;
            const groupId = document.getElementById('group-select').value;
            const teacherId = document.getElementById('teacher-select').value;
            const year = document.getElementById('year-select').value;
            
            // Update state with single selections
            this.state.selectedFilters = {
                schoolIds: schoolId ? [parseInt(schoolId)] : [],
                groupIds: groupId ? [parseInt(groupId)] : [],
                teacherIds: teacherId ? [parseInt(teacherId)] : [],
                years: year ? [parseInt(year)] : []
            };
            
            // Fetch schedule
            const schedule = await this.fetchSchedule(this.state.selectedFilters);
            this.state.currentSchedule = schedule;
            
            // Switch to schedule view
            this.switchToScheduleView();
            this.renderSchedule(schedule);
            
        } catch (error) {
            this.showError('Błąd pobierania planu: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    switchToScheduleView() {
        document.getElementById('filters-section').style.display = 'none';
        document.getElementById('schedule-section').style.display = 'block';
        
        // Update title
        const title = this.generateScheduleTitle();
        document.getElementById('schedule-title').textContent = title;
    }
    
    switchToFiltersView() {
        document.getElementById('schedule-section').style.display = 'none';
        document.getElementById('filters-section').style.display = 'block';
        document.getElementById('options-panel').style.display = 'none';
        
        // Update form values from current state
        this.updateFormFromState();
    }
    
    updateFormFromState() {
        const filters = this.state.selectedFilters;
        
        // Update simple selects with first selected item (if any)
        document.getElementById('school-select').value = filters.schoolIds[0] || '';
        document.getElementById('group-select').value = filters.groupIds[0] || '';
        document.getElementById('teacher-select').value = filters.teacherIds[0] || '';
        document.getElementById('year-select').value = filters.years[0] || '';
        
        // Trigger school change to update dependent selects
        if (filters.schoolIds.length > 0) {
            this.onSchoolChange(filters.schoolIds[0]);
        }
    }
    
    generateScheduleTitle() {
        const filters = this.state.selectedFilters;
        let title = 'Plan zajęć';
        
        if (filters.schoolIds.length > 0) {
            if (filters.schoolIds.length === 1) {
                const school = this.state.schools.find(s => s.id === filters.schoolIds[0]);
                if (school) title += ` - ${school.name}`;
            } else {
                title += ` - ${filters.schoolIds.length} szkół`;
            }
        }
        
        if (filters.groupIds.length > 0) {
            if (filters.groupIds.length === 1) {
                const group = this.state.groups.find(g => g.id === filters.groupIds[0]);
                if (group) title += ` - Klasa ${group.name}`;
            } else {
                title += ` - ${filters.groupIds.length} klas`;
            }
        }
        
        if (filters.teacherIds.length > 0) {
            if (filters.teacherIds.length === 1) {
                const teacher = this.state.teachers.find(t => t.id === filters.teacherIds[0]);
                if (teacher) title += ` - ${teacher.name} ${teacher.surname}`;
            } else {
                title += ` - ${filters.teacherIds.length} nauczycieli`;
            }
        }
        
        if (filters.years.length > 0) {
            if (filters.years.length === 1) {
                title += ` - Rok ${filters.years[0]}`;
            } else {
                title += ` - ${filters.years.length} lat`;
            }
        }
        
        return title;
    }
    
    async toggleOptionsPanel(force = null) {
        const panel = document.getElementById('options-panel');
        const isVisible = panel.style.display === 'block';
        
        if (force !== null) {
            panel.style.display = force ? 'block' : 'none';
        } else {
            panel.style.display = isVisible ? 'none' : 'block';
        }
        
        if (panel.style.display === 'block') {
            await this.loadOptionsData();
            this.renderOptionsPanel();
        }
    }
    
    async loadOptionsData() {
        try {
            // Load all data for options if not already loaded
            if (this.state.schools.length === 0) {
                this.state.schools = await this.fetchAPI('/api/schools');
            }
            
            if (this.state.groups.length === 0) {
                this.state.groups = await this.fetchAPI('/api/groups');
            }
            
            if (this.state.teachers.length === 0) {
                this.state.teachers = await this.fetchAPI('/api/teachers');
            }
            
            if (this.state.years.length === 0) {
                this.state.years = await this.fetchAPI('/api/years');
            }
        } catch (error) {
            this.showError('Błąd ładowania opcji: ' + error.message);
        }
    }
    
    renderOptionsPanel() {
        this.renderOptionsList('schools-options', this.state.schools, 'schoolIds', 'name');
        this.renderOptionsList('groups-options', this.state.groups, 'groupIds', 'name', (group) => 
            `${group.name} (${group.school_name})`);
        this.renderOptionsList('teachers-options', this.state.teachers, 'teacherIds', null, (teacher) => 
            `${teacher.name} ${teacher.surname} (${teacher.school_name})`);
        this.renderOptionsList('years-options', this.state.years, 'years', null, null, true);
    }
    
    renderOptionsList(containerId, items, filterKey, labelKey, labelFn = null, isSimpleArray = false) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        
        items.forEach(item => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option-item';
            
            const value = isSimpleArray ? item : item.id;
            const isSelected = this.state.selectedFilters[filterKey].includes(value);
            
            if (isSelected) {
                optionDiv.classList.add('selected');
            }
            
            let label;
            if (isSimpleArray) {
                label = item.toString();
            } else if (labelFn) {
                label = labelFn(item);
            } else {
                label = item[labelKey];
            }
            
            optionDiv.innerHTML = `
                <div class="option-checkbox"></div>
                <div class="option-text">${label}</div>
            `;
            
            optionDiv.addEventListener('click', () => {
                this.toggleOptionSelection(filterKey, value, optionDiv);
            });
            
            container.appendChild(optionDiv);
        });
    }
    
    toggleOptionSelection(filterKey, value, element) {
        const isCurrentlySelected = element.classList.contains('selected');
        const currentSelection = this.state.selectedFilters[filterKey];
        
        if (isCurrentlySelected) {
            // Deselect - remove from array
            const index = currentSelection.indexOf(value);
            if (index > -1) {
                currentSelection.splice(index, 1);
            }
            element.classList.remove('selected');
        } else {
            // Select - add to array
            if (!currentSelection.includes(value)) {
                currentSelection.push(value);
            }
            element.classList.add('selected');
        }
    }
    
    async applyFilters() {
        this.toggleOptionsPanel(false);
        
        try {
            this.showLoading(true);
            
            const schedule = await this.fetchSchedule(this.state.selectedFilters);
            this.state.currentSchedule = schedule;
            
            // Update title and render
            const title = this.generateScheduleTitle();
            document.getElementById('schedule-title').textContent = title;
            this.renderSchedule(schedule);
            
        } catch (error) {
            this.showError('Błąd filtrowania planu: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    clearFilters() {
        this.state.selectedFilters = {
            schoolIds: [],
            groupIds: [],
            teacherIds: [],
            years: []
        };
        
        this.renderOptionsPanel();
    }
    
    async fetchSchedule(filters) {
        const params = new URLSearchParams();
        
        // Add multiple values for each filter type
        filters.schoolIds.forEach(id => params.append('school_id', id));
        filters.groupIds.forEach(id => params.append('group_id', id));
        filters.teacherIds.forEach(id => params.append('teacher_id', id));
        filters.years.forEach(year => params.append('year', year));
        
        return await this.fetchAPI(`/api/schedule?${params.toString()}`);
    }
    
    renderSchedule(scheduleData) {
        const container = document.getElementById('schedule-content');
        
        if (!scheduleData || Object.keys(scheduleData).length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>Brak danych</h3>
                    <p>Nie znaleziono planu dla wybranych kryteriów</p>
                </div>
            `;
            return;
        }
        
        let html = '<div class="schedule-grid">';
        
        Object.entries(scheduleData).forEach(([key, classData]) => {
            html += this.renderClassSchedule(classData);
        });
        
        html += '</div>';
        container.innerHTML = html;
    }
    
    renderClassSchedule(classData) {
        const days = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'];
        const times = [
            '8:00-8:45', '8:55-9:40', '9:50-10:35', '10:45-11:30',
            '11:40-12:25', '12:35-13:20', '13:30-14:15', '14:25-15:10',
            '15:20-16:05', '16:15-17:00'
        ];
        
        const isGeneralView = classData.is_general_view;
        
        let html = `
            <div class="class-schedule ${isGeneralView ? 'general-view' : ''}">
                <div class="class-header">
                    <h3>${classData.group_name}</h3>
                    <div class="class-info">${classData.school_name}</div>
                </div>
                <table class="schedule-table">
                    <thead>
                        <tr>
                            <th>Godzina</th>
                            ${days.map(day => `<th>${day}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        times.forEach(time => {
            html += `<tr>`;
            html += `<td class="time-cell">${time}</td>`;
            
            days.forEach(day => {
                const lessons = classData.schedule[time] && classData.schedule[time][day];
                html += `<td class="lesson-cell">`;
                
                if (lessons && lessons.length > 0) {
                    if (Array.isArray(lessons)) {
                        // Multiple lessons (general view)
                        lessons.forEach(lesson => {
                            html += `
                                <div class="lesson-card">
                                    <div class="lesson-subject">${lesson.course}</div>
                                    <div class="lesson-teacher">${lesson.teacher}</div>
                                    <div class="lesson-room">Sala: ${lesson.classroom}</div>
                                    <div class="lesson-group">Klasa: ${lesson.group}</div>
                                    <div class="lesson-school">${lesson.school}</div>
                                </div>
                            `;
                        });
                    } else {
                        // Single lesson (specific class view)
                        html += `
                            <div class="lesson-card">
                                <div class="lesson-subject">${lessons.course}</div>
                                <div class="lesson-teacher">${lessons.teacher}</div>
                                <div class="lesson-room">Sala: ${lessons.classroom}</div>
                            </div>
                        `;
                    }
                } else {
                    html += `<div class="empty-cell">—</div>`;
                }
                
                html += `</td>`;
            });
            
            html += `</tr>`;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        return html;
    }
    
    // Utility methods
    async fetchAPI(url) {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    }
    
    populateSelect(selectId, items, valueKey, labelKey, isSimpleArray = false, labelFn = null) {
        const select = document.getElementById(selectId);
        const firstOption = select.options[0];
        
        select.innerHTML = '';
        select.appendChild(firstOption);
        
        items.forEach(item => {
            const option = document.createElement('option');
            
            if (isSimpleArray) {
                option.value = item;
                option.textContent = item;
            } else {
                option.value = item[valueKey];
                option.textContent = labelFn ? labelFn(item) : item[labelKey];
            }
            
            select.appendChild(option);
        });
    }
    
    clearSelect(selectId, placeholderText) {
        const select = document.getElementById(selectId);
        select.innerHTML = `<option value="">${placeholderText}</option>`;
    }
    
    updateUI() {
        const showButton = document.getElementById('show-schedule-btn');
        showButton.disabled = false; // Always allow showing schedule
    }
    
    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        this.state.isLoading = show;
        
        if (show) {
            overlay.classList.add('show');
        } else {
            overlay.classList.remove('show');
        }
    }
    
    showError(message) {
        const notification = document.getElementById('error-notification');
        const messageElement = document.getElementById('error-message');
        
        messageElement.textContent = message;
        notification.classList.add('show');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }
    
    hideError() {
        const notification = document.getElementById('error-notification');
        notification.classList.remove('show');
    }
}

// Global functions for HTML event handlers
function hideError() {
    if (window.scheduleApp) {
        window.scheduleApp.hideError();
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.scheduleApp = new ScheduleApp();
});