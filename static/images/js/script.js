document.addEventListener('DOMContentLoaded', function() {
    //for add subject popup
    const subject = document.querySelector(".subject");
    const showsub = document.querySelector(".showSub");
    const closesub = document.querySelectorAll(".closeSub");
  
    showsub.addEventListener("click", function () {
      subject.classList.remove("hidden");
      subject.classList.add("flex");
    });
    closesub.forEach((close) => {
      close.addEventListener("click", function () {
        subject.classList.add("hidden");
      });
    });
});
  