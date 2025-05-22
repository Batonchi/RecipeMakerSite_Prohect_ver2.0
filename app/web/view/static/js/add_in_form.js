export class AddInForm {
    static async fetchTemplate(type, params = {}) {
        const url = new URL(`/recipe/form/get-${type}-form`, window.location.origin);
        Object.entries(params).forEach(([key, value]) => {
            url.searchParams.append(key, value);
        });

        const response = await fetch(url);
        return await response.text();
    }

    static initImageHandlers() {
        // Обработчик для существующих кнопок добавления изображений
        document.querySelectorAll('.button--add_images').forEach(button => {
            // Проверяем, что кнопка существует в DOM
            if (!button || !button.parentNode) return;

            // Клонируем кнопку и заменяем оригинал
            const newButton = button.cloneNode(true);
            button.replaceWith(newButton);

            const stepIndex = newButton.getAttribute('data-step-index');
            newButton.addEventListener('click', function (e) {
                e.stopPropagation();
                const fileInput = document.createElement('input');
                fileInput.type = 'file';
                fileInput.accept = 'image/*';
                fileInput.multiple = true;

                fileInput.addEventListener('change', function (e) {
                    const files = e.target.files;
                    const container = document.getElementById(`container_graph-${stepIndex}`);
                    if (!container) return;

                    for (let i = 0; i < files.length; i++) {
                        const file = files[i];
                        const reader = new FileReader();

                        reader.onload = function (e) {
                            const imageDiv = document.createElement('div');
                            imageDiv.className = 'image-item';

                            const imgPreview = document.createElement('img');
                            imgPreview.src = e.target.result;
                            imgPreview.style.maxWidth = '100px';
                            imgPreview.style.maxHeight = '100px';

                            const deleteButton = document.createElement('button');
                            deleteButton.textContent = '×';
                            deleteButton.className = 'delete-image-button';
                            deleteButton.addEventListener('click', (e) => {
                                e.stopPropagation();
                                imageDiv.remove();
                            });

                            imageDiv.appendChild(imgPreview);
                            imageDiv.appendChild(deleteButton);
                            container.appendChild(imageDiv);
                        };
                        reader.readAsDataURL(file);
                    }
                });

                fileInput.click();
            });
        });
    }


    static async addStep(container, index) {
        const html = await this.fetchTemplate('step', {index});
        const template = document.createElement('template');
        template.innerHTML = html.trim();
        const stepElement = template.content.firstChild;

        // Устанавливаем data-атрибут с индексом
        stepElement.setAttribute('data-step-index', index);

        // Вставляем перед кнопкой добавления
        container.insertBefore(stepElement, container.querySelector('.add-button'));

        // Инициализация обработчиков для нового шага
        this.initStepHandlers(stepElement);
        return stepElement;
    }

    static async addIngredient(container, index) {
        const html = await this.fetchTemplate('ingredient', {index});
        const template = document.createElement('template');
        template.innerHTML = html.trim();
        const ingredientElement = template.content.firstChild;

        // Обновляем номер ингредиента
        const idLabel = ingredientElement.querySelector('.id_ing');
        if (idLabel) idLabel.textContent = index + 1;

        // Обновляем имена полей
        ingredientElement.querySelectorAll('input').forEach(input => {
            input.name = input.name.replace(/ingredients-\d+/, `ingredients-${index}`);
        });

        container.appendChild(ingredientElement);
        return ingredientElement;
    }

    static async addStepLink(stepIndex, linkIndex) {
        const stepElement = document.querySelector(`.steps__elem[data-step-index="${stepIndex}"]`);
        if (!stepElement) return;

        const container = stepElement.querySelector('.links--add .container');
        if (!container) return;

        const html = await this.fetchTemplate('link', {
            step_index: stepIndex,
            link_index: linkIndex
        });
        const template = document.createElement('template');
        template.innerHTML = html.trim();
        const linkElement = template.content.firstChild;
        container.appendChild(linkElement);
        return linkElement;
    }

    static async addRecipeLink(linkIndex) {
        const container = document.getElementById('all_links');
        if (!container) return;

        const html = await this.fetchTemplate('recipe-link', {link_index: linkIndex});
        const template = document.createElement('template');
        template.innerHTML = html.trim();
        const linkElement = template.content.firstChild;
        container.appendChild(linkElement);
        return linkElement;
    }

    static initRecipeLinkHandlers() {
        // Обработчик добавления ссылок рецепта
        document.querySelector('.hyper_text_link__button')?.addEventListener('click', async () => {
            const container = document.getElementById('all_links');
            const linkCount = container.querySelectorAll('.link').length;
            await this.addRecipeLink(linkCount);
        });

        // Инициализация обработчиков для существующих ссылок рецепта
        document.querySelectorAll('#all_links .label__button--delete_link').forEach(button => {
            button.addEventListener('click', function () {
                this.closest('.link').remove();
                AddInForm.updateIndexes();
            });
        });
    }

    static initStepHandlers(stepElement) {
        const stepIndex = this.getStepIndex(stepElement);

        // Обработчик добавления ссылок для шага
        const addLinkButton = stepElement.querySelector('.add--step_link__button');
        if (addLinkButton && addLinkButton.parentNode) {
            const newLinkButton = addLinkButton.cloneNode(true);
            addLinkButton.replaceWith(newLinkButton);

            newLinkButton.addEventListener('click', async (e) => {
                e.stopPropagation();
                const linkCount = stepElement.querySelectorAll('.link').length;
                await this.addStepLink(stepIndex, linkCount);
            });
        }

        // Обработчик добавления изображений
        const addImageButton = stepElement.querySelector('.button--add_images');
        if (addImageButton && addImageButton.parentNode) {
            const newImageButton = addImageButton.cloneNode(true);
            newImageButton.setAttribute('data-step-index', stepIndex);
            addImageButton.replaceWith(newImageButton);

            newImageButton.addEventListener('click', function (e) {
                e.stopPropagation();
                const fileInput = document.createElement('input');
                fileInput.type = 'file';
                fileInput.accept = 'image/*';
                fileInput.multiple = true;

                fileInput.addEventListener('change', function (e) {
                    const files = e.target.files;
                    const container = document.getElementById(`container_graph-${stepIndex}`);
                    if (!container) return;

                    for (let i = 0; i < files.length; i++) {
                        const file = files[i];
                        const reader = new FileReader();

                        reader.onload = function (e) {
                            const imageDiv = document.createElement('div');
                            imageDiv.className = 'image-item';

                            const imgPreview = document.createElement('img');
                            imgPreview.src = e.target.result;
                            imgPreview.style.maxWidth = '100px';
                            imgPreview.style.maxHeight = '100px';

                            const deleteButton = document.createElement('button');
                            deleteButton.textContent = '×';
                            deleteButton.className = 'delete-image-button';
                            deleteButton.addEventListener('click', (e) => {
                                e.stopPropagation();
                                imageDiv.remove();
                            });

                            imageDiv.appendChild(imgPreview);
                            imageDiv.appendChild(deleteButton);
                            container.appendChild(imageDiv);
                        };
                        reader.readAsDataURL(file);
                    }
                });

                fileInput.click();
            });
        }
    }

    static getStepIndex(stepElement) {
        // Сначала пробуем получить из data-атрибута
        const dataIndex = stepElement.getAttribute('data-step-index');
        if (dataIndex) return parseInt(dataIndex);

        // Если нет, то из имени поля
        const nameAttr = stepElement.querySelector('[name^="steps-"]')?.name;
        return nameAttr ? parseInt(nameAttr.match(/steps-(\d+)/)[1]) : 0;
    }

    static initDeleteHandlers() {
        document.addEventListener('click', (e) => {
            // Удаление шага
            if (e.target.classList.contains('step__elem--del')) {
                e.target.closest('.steps__elem').remove();
                this.updateIndexes();
            }

            // Удаление ингредиента
            if (e.target.classList.contains('label__button--delete_ing')) {
                e.target.closest('.ingredient').remove();
                this.updateIndexes();
            }

            // Удаление ссылки
            if (e.target.classList.contains('label__button--delete_link')) {
                e.target.closest('.link').remove();
                this.updateIndexes();
            }
        });
    }

    static updateIndexes() {
        // Обновление индексов ингредиентов
        document.querySelectorAll('.ingredient').forEach((ing, idx) => {
            const idLabel = ing.querySelector('.id_ing');
            if (idLabel) idLabel.textContent = idx + 1;

            ing.querySelectorAll('input').forEach(input => {
                input.name = input.name.replace(/ingredients-\d+/, `ingredients-${idx}`);
            });
        });

        // Обновление индексов шагов и их ссылок
        document.querySelectorAll('.steps__elem').forEach((step, stepIdx) => {
            // Устанавливаем data-атрибут с индексом
            step.setAttribute('data-step-index', stepIdx);

            // Обновляем индексы полей шага
            step.querySelectorAll('[name^="steps-"]').forEach(field => {
                field.name = field.name.replace(/steps-\d+/, `steps-${stepIdx}`);
            });

            // Обновляем индексы контейнеров
            const containers = step.querySelectorAll('[id^="step_links-"], [id^="container_graph-"]');
            containers.forEach(container => {
                container.id = container.id.replace(/\d+/, stepIdx);
            });

            // Обновляем data-атрибуты кнопок
            const buttons = step.querySelectorAll('[data-step-index]');
            buttons.forEach(button => {
                button.setAttribute('data-step-index', stepIdx);
            });

            // Обновляем индексы ссылок
            step.querySelectorAll('.link').forEach((link, linkIdx) => {
                link.querySelectorAll('input').forEach(input => {
                    input.name = input.name
                        .replace(/steps-\d+-links-\d+/, `steps-${stepIdx}-links-${linkIdx}`);
                });
            });
        });

        // Обновление индексов ссылок рецепта
        document.querySelectorAll('#all_links .link').forEach((link, linkIdx) => {
            link.querySelectorAll('input').forEach(input => {
                input.name = input.name
                    .replace(/links-\d+/, `links-${linkIdx}`);
            });
        });
    }

    static async addInitialElements() {
        // Добавляем первый ингредиент, если контейнер пуст
        const ingredientsContainer = document.getElementById('cont_ing');
        if (ingredientsContainer && ingredientsContainer.children.length === 0) {
            await this.addIngredient(ingredientsContainer, 0);
        }

        // Добавляем первый шаг, если контейнер пуст
        const stepsContainer = document.querySelector('.steps .block--flex_column');
        if (stepsContainer && stepsContainer.querySelectorAll('.steps__elem').length === 0) {
            await this.addStep(stepsContainer, 0);
        }

        // Добавляем первую ссылку рецепта, если контейнер пуст
        const recipeLinksContainer = document.getElementById('all_links');
        if (recipeLinksContainer && recipeLinksContainer.children.length === 0) {
            await this.addRecipeLink(0);
        }

        // Инициализация обработчиков
        this.initImageHandlers();
        this.initRecipeLinkHandlers();
    }

    static initAddButtons() {
        // Кнопка добавления ингредиента
        document.querySelector('.plus_ing')?.addEventListener('click', async () => {
            const container = document.getElementById('cont_ing');
            const index = container.children.length;
            await this.addIngredient(container, index);
        });

        // Кнопка добавления шага
        document.querySelector('.steps .add-button')?.addEventListener('click', async () => {
            const container = document.querySelector('.steps .block--flex_column');
            const index = container.querySelectorAll('.steps__elem').length;
            await this.addStep(container, index);
        });
    }
}

// Инициализация формы при загрузке
document.addEventListener('DOMContentLoaded', async () => {
    await AddInForm.addInitialElements();
    AddInForm.initAddButtons();
    AddInForm.initDeleteHandlers();

    // Инициализация обработчиков для существующих шагов
    document.querySelectorAll('.steps__elem').forEach(step => {
        AddInForm.initStepHandlers(step);
    });
});