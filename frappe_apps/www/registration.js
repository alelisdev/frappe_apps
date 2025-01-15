frappe.ready(function () {
    $('#registration-form').off('submit').on('submit', function (e) {
        e.preventDefault();

        const first_name = $('[name="first_name"]').val();
        const last_name = $('[name="last_name"]').val();
        const email = $('[name="email"]').val();
        const phone = $('[name="phone"]').val();
        const password = $('[name="password"]').val();
        const confirmpassword = $('[name="confirmpassword"]').val();
        const date_of_birth = $('[name="date_of_birth"]').val();
        const date_of_joining = $('[name="date_of_joining"]').val();
        const gender = $('[name="gender"]').val();

        if (password !== confirmpassword) {
            frappe.msgprint("Password doesn't match.");
            return; 
        }

        frappe.call({
            method: 'frappe_apps.www.registration.get_response',
            args: {
                first_name: first_name,
                last_name: last_name,
                email: email,
                phone: phone,
                password: password,
                date_of_birth: date_of_birth,
                date_of_joining: date_of_joining,
                gender: gender,
            },
            headers: {
                'X-Frappe-CSRF-Token': frappe.csrf_token, 
            },
            callback: function (r) {
                if (r.message === 'COMPLETE_DATA') {
                    frappe.msgprint('Thanks for your joining.');
                    $(':input').val(''); 
                } else {
                    frappe.msgprint(r.message);
                }
            },
            error: function (err) {
                console.error('Error occurred:', err);
                frappe.msgprint('Something went wrong. Please try again.');
            },
        });
    });
});
