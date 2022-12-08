// Получаем все необходимые объекты через id
const hamb = document.querySelector("#hamb");
const popup = document.querySelector("#popup");
const body = document.body;
// Клон меню, который мы вставим в popup
const menu = document.querySelector("#menu").cloneNode(1);
// Получаем список ссылок из меню
const links = Array.from(menu.children);

// Создаём обработчик событий при клике, вызываем функцию hambHandler
hamb.addEventListener("click", hambHandler);

function hambHandler(e){
	// Сбрасываем стандартное поведение кнопки
	e.preventDefault();
	// Переключаем стили элементов при клике
	popup.classList.toggle("open");
	hamb.classList.toggle("active");
	body.classList.toggle("noscroll");
	renderPopup();
}

// Функция для добавления меню в popup
function renderPopup(){
	popup.appendChild(menu);
}

// Для каждой ссылки создаём обработчик событий с помощью цикла
links.forEach((link) => {
  link.addEventListener("click", closeOnClick);
});

function closeOnClick() {
  popup.classList.remove("open");
  hamb.classList.remove("active");
  body.classList.remove("noscroll");
}