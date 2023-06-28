function my_scope() {
    const forms = document.querySelectorAll('.form-delete');
  
    for (const form of forms) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
  
        const confirmed = confirm('Confirm delete your recipe ?');
  
        if (confirmed) {
          form.submit();
        }
      });
    }
  }
  
  my_scope();