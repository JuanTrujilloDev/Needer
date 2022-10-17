var search_input = document.getElementById("search_form")


search_input.addEventListener("keydown", function (e){
    if(e.code === "Enter" && !e.shiftKey) {
        e.preventDefault();
    
        $(this).closest("form").submit();
    }
  });