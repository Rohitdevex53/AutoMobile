$(document).ready(function() {
    // Current page state
    let currentPageUsers = 1;
    let currentPageMechanics = 1;

    // Initial loads
    fetchStats();
    fetchUsers(null, '#summary-user-table-body', 1); // Dashboard summary

    // Navigation logic
    $('.nav-link').click(function(e) {
        e.preventDefault();
        const linkId = $(this).attr('id');
        const sectionId = linkId.replace('link-', 'section-');
        
        switchSection(sectionId);
        
        // Load data specific to section
        if (sectionId === 'section-dashboard') {
            fetchStats();
            fetchUsers(null, '#summary-user-table-body', 1);
        } else if (sectionId === 'section-users') {
            fetchUsers(null, '#full-user-table-body', currentPageUsers);
        } else if (sectionId === 'section-mechanics') {
            fetchUsers('mechanic', '#mechanic-table-body', currentPageMechanics);
        }
    });

    function switchSection(sectionId) {
        $('.nav-link').removeClass('active');
        $(`#link-${sectionId.replace('section-', '')}`).addClass('active');
        $('.dashboard-section').hide();
        $(`#${sectionId}`).fadeIn(300);
    }

    // Stats fetching
    function fetchStats() {
        $.ajax({
            url: '/auth/admin/stats/',
            type: 'GET',
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') },
            success: function(data) {
                $('#total-users').text(data.total_users);
                $('#total-customers').text(data.customers);
                $('#total-mechanics').text(data.mechanics);
                $('#pending-active').text(data.pending_active);
            }
        });
    }

    // User list fetching
    function fetchUsers(role, tableBodyId, page = 1) {
        let url = `/auth/admin/users/?page=${page}`;
        if (role) {
            url += `&role=${role}`;
        }

        $.ajax({
            url: url,
            type: 'GET',
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') },
            success: function(data) {
                const tbody = $(tableBodyId);
                tbody.empty();
                
                // DRF Paginated response has results key
                const userList = data.results || data;
                
                // Dashboard summary: only show first 5
                const displayData = tableBodyId === '#summary-user-table-body' ? userList.slice(0, 5) : userList;

                if (!displayData || displayData.length === 0) {
                    tbody.append('<tr><td colspan="4" class="text-center py-4 text-dim">No users found</td></tr>');
                    return;
                }

                displayData.forEach(user => {
                    const row = `
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    <div class="status-indicator ${user.is_active ? 'status-active' : 'status-inactive'}"></div>
                                    <div>
                                        <div class="fw-semibold">${user.name}</div>
                                        <div class="text-dim small">${user.email}</div>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <span class="role-badge badge-${user.role}">${user.role.charAt(0).toUpperCase() + user.role.slice(1)}</span>
                            </td>
                            <td>${new Date(user.created_at).toLocaleDateString()}</td>
                            <td>
                                <button class="btn-action toggle-active" data-id="${user.id}" data-table="${tableBodyId}" data-role="${role}" data-page="${page}">
                                    ${user.is_active ? 'Deactivate' : 'Activate'}
                                </button>
                            </td>
                        </tr>
                    `;
                    tbody.append(row);
                });

                // Update pagination controls if NOT the dashboard summary
                if (tableBodyId !== '#summary-user-table-body') {
                    const section = tableBodyId === '#full-user-table-body' ? 'users' : 'mechanics';
                    updatePaginationUI(section, data, page);
                }
            }
        });
    }

    function updatePaginationUI(section, data, page) {
        const infoText = $(`#${section}-pagination-info`);
        infoText.text(`Showing page ${page}`);

        const prevBtn = $(`.prev-page[data-section="${section}"]`);
        const nextBtn = $(`.next-page[data-section="${section}"]`);

        // Enable/Disable buttons based on DRF response
        prevBtn.prop('disabled', !data.previous);
        nextBtn.prop('disabled', !data.next);
    }

    // Pagination events
    $(document).on('click', '.next-page', function() {
        const section = $(this).data('section');
        if (section === 'users') {
            currentPageUsers++;
            fetchUsers(null, '#full-user-table-body', currentPageUsers);
        } else {
            currentPageMechanics++;
            fetchUsers('mechanic', '#mechanic-table-body', currentPageMechanics);
        }
    });

    $(document).on('click', '.prev-page', function() {
        const section = $(this).data('section');
        if (section === 'users') {
            if (currentPageUsers > 1) {
                currentPageUsers--;
                fetchUsers(null, '#full-user-table-body', currentPageUsers);
            }
        } else {
            if (currentPageMechanics > 1) {
                currentPageMechanics--;
                fetchUsers('mechanic', '#mechanic-table-body', currentPageMechanics);
            }
        }
    });

    // Toggle user status
    $(document).on('click', '.toggle-active', function() {
        const userId = $(this).data('id');
        const tableBodyId = $(this).data('table');
        const role = $(this).data('role');
        const page = $(this).data('page');
        const btn = $(this);
        btn.prop('disabled', true).text('...');

        $.ajax({
            url: `/auth/admin/users/${userId}/toggle-active/`,
            type: 'POST',
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') },
            success: function() {
                fetchStats();
                fetchUsers(role, tableBodyId, page);
            }
        });
    });

    // Logout
    $('#logout-btn').click(function(e) {
        e.preventDefault();
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login/';
    });
});
