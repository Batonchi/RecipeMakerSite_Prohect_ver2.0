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
        document.addEventListener('click', async (e) => {
            if (e.target.classList.contains('button--add_images')) {
                const stepIndex = e.target.dataset.stepIndex;
                await this.handleImageUpload(stepIndex);
            }
        });
    }

    static initStepHandlers(stepElement) {
        const stepIndex = this.getStepIndex(stepElement);

        // Обработчик кнопки добавления ссылки
        const addLinkButton = stepElement.querySelector('.add--step_link__button');
        if (addLinkButton) {
            addLinkButton.addEventListener('click', async (e) => {
                e.stopPropagation();
                const linkCount = stepElement.querySelectorAll('.link').length;
                await this.addStepLink(stepIndex, linkCount);
            });
        }

        // Обработчик кнопки добавления изображений
        const addImageButton = stepElement.querySelector('.button--add_images');
        if (addImageButton) {
            addImageButton.setAttribute('data-step-index', stepIndex);
            addImageButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.handleImageUpload(stepIndex);
            });
        }
    }

    static getStepIndex(stepElement) {
        if (stepElement.hasAttribute('data-step-index')) {
            return parseInt(stepElement.getAttribute('data-step-index'));
        }

        const nameAttr = stepElement.querySelector('[name^="steps-"]')?.name;
        if (nameAttr) {
            const match = nameAttr.match(/steps-(\d+)/);
            return match ? parseInt(match[1]) : 0;
        }

        return 0;
    }

    static async handleImageUpload(stepIndex) {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.multiple = true;
        fileInput.name = `steps-${stepIndex}-images`; // Важно для FormData

        fileInput.addEventListener('change', async (e) => {
            const files = Array.from(e.target.files);
            const container = document.getElementById(`container_graph-${stepIndex}`);

            if (!container) return;

            // Создаем скрытый input для хранения файлов
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = `steps-${stepIndex}-image-filenames`;
            hiddenInput.className = 'image-filenames';
            container.appendChild(hiddenInput);

            // Предзагрузка файлов на сервер
            const filenames = await this.uploadImages(files, stepIndex);
            hiddenInput.value = JSON.stringify(filenames);

            // Показываем превью
            files.forEach((file, index) => {
                const reader = new FileReader();
                reader.onload = (event) => {
                    const imageDiv = document.createElement('div');
                    imageDiv.className = 'image-item';
                    imageDiv.dataset.filename = filenames[index];

                    const img = document.createElement('img');
                    img.src = event.target.result;
                    img.style.maxWidth = '100px';
                    img.style.maxHeight = '100px';

                    const deleteBtn = document.createElement('button');
                    deleteBtn.textContent = '×';
                    deleteBtn.className = 'delete-image-button';
                    deleteBtn.addEventListener('click', async () => {
                        await this.deleteImage(filenames[index]);
                        imageDiv.remove();
                    });

                    imageDiv.appendChild(img);
                    imageDiv.appendChild(deleteBtn);
                    container.appendChild(imageDiv);
                };
                reader.readAsDataURL(file);
            });
        });

        fileInput.click();
    }

    static async uploadImages(files, stepIndex) {
        const formData = new FormData();
        files.forEach(file => {
            formData.append('images', file);
        });
        formData.append('step_index', stepIndex);

        try {
            const response = await fetch('/form/upload-images', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]')?.value || '',
                }
            });
            const result = await response.json();
            if (response.ok) {
                return result.filenames;
            } else {
                console.error('Upload error:', result.error);
                return [];
            }
        } catch (error) {
            console.error('Upload failed:', error);
            return [];
        }
    }

    static async deleteImage(filename) {
        try {
            await fetch('/form/delete-image', {
                method: 'POST',
                body: JSON.stringify({filename}),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]')?.value || '',
                }
            });
        } catch (error) {
            console.error('Delete failed:', error);
        }
    }

    static async addStep(container, index) {
        try {
            const html = await this.fetchTemplate('step', {index});
            const template = document.createElement('template');
            template.innerHTML = html.trim();
            const stepElement = template.content.firstChild;

            // Устанавливаем индекс шага
            stepElement.setAttribute('data-step-index', index);

            // Находим контейнер для шагов
            const stepsContainer = container.querySelector('.steps-container') || container;

            // Находим кнопку добавления
            const addButton = stepsContainer.querySelector('.add-button') ||
                stepsContainer.querySelector('#add_step');

            if (addButton && addButton.parentNode === stepsContainer) {
                stepsContainer.insertBefore(stepElement, addButton);
            } else {
                stepsContainer.appendChild(stepElement);
            }

            // Инициализируем обработчики
            this.initStepHandlers(stepElement);
            return stepElement;
        } catch (error) {
            console.error('Error adding step:', error);
            return null;
        }
    }

    static async addIngredient(container, index) {
        const html = await this.fetchTemplate('ingredient', {index});
        const template = document.createElement('template');
        template.innerHTML = html.trim();
        const ingredientElement = template.content.firstChild;

        const idLabel = ingredientElement.querySelector('.id_ing');
        if (idLabel) idLabel.textContent = index + 1;

        ingredientElement.querySelectorAll('input').forEach(input => {
            input.name = input.name.replace(/ingredients-\d+/, `ingredients-${index}`);
            if (input.name.includes('for_what') && input.value === 'None') {
                input.value = '';
            }
        });

        container.appendChild(ingredientElement);
        return ingredientElement;
    }

    static async addStepLink(stepIndex, linkIndex) {
        try {
            const stepElement = document.querySelector(`.steps__elem[data-step-index="${stepIndex}"]`);
            if (!stepElement) {
                console.error(`Step element with index ${stepIndex} not found`);
                return;
            }

            const container = stepElement.querySelector('.links--add .container');
            if (!container) {
                console.error('Links container not found in step element');
                return;
            }

            const html = await this.fetchTemplate('link', {
                step_index: stepIndex,
                link_index: linkIndex
            });

            const template = document.createElement('template');
            template.innerHTML = html.trim();
            const linkElement = template.content.firstChild;

            container.appendChild(linkElement);
            return linkElement;
        } catch (error) {
            console.error('Error adding step link:', error);
        }
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
        document.addEventListener('click', (e) => {
            if (e.target.id === 'add_recipe_link' || e.target.classList.contains('hyper_text_link__button')) {
                const container = document.getElementById('all_links');
                const linkCount = container.querySelectorAll('.link').length;
                this.addRecipeLink(linkCount);
            }
        });
    }

    static initDeleteHandlers() {
        document.addEventListener('click', (e) => {
            // Удаление шага
            if (e.target.classList.contains('step__elem--del')) {
                e.target.closest('.steps__elem').remove();
                this.updateIndexes();
                return;
            }

            // Удаление ингредиента
            if (e.target.classList.contains('label__button--delete_ing')) {
                e.target.closest('.ingredient').remove();
                this.updateIndexes();
                return;
            }

            // Удаление ссылки
            if (e.target.classList.contains('label__button--delete_link')) {
                e.target.closest('.link').remove();
                this.updateIndexes();
                return;
            }

            // Удаление изображения
            if (e.target.classList.contains('delete-image-button')) {
                e.target.closest('.image-item').remove();
                return;
            }
        });
    }

    static updateIndexes() {
        // Обновление индексов ингредиентов
        document.querySelectorAll('#cont_ing .ingredient').forEach((ing, idx) => {
            const idLabel = ing.querySelector('.id_ing');
            if (idLabel) idLabel.textContent = idx + 1;

            ing.querySelectorAll('input').forEach(input => {
                input.name = input.name.replace(/ingredients-\d+/, `ingredients-${idx}`);
            });
        });

        // Обновление индексов шагов
        document.querySelectorAll('#cont_steps .steps__elem').forEach((step, stepIdx) => {
            step.dataset.stepIndex = stepIdx;

            step.querySelectorAll('[name^="steps-"]').forEach(field => {
                field.name = field.name.replace(/steps-\d+/, `steps-${stepIdx}`);
            });

            // Обновляем контейнеры изображений и ссылок
            const containers = step.querySelectorAll('[id^="step_links-"], [id^="container_graph-"]');
            containers.forEach(container => {
                container.id = container.id.replace(/\d+/, stepIdx);
            });

            // Обновляем data-атрибуты кнопок
            const buttons = step.querySelectorAll('[data-step-index]');
            buttons.forEach(button => {
                button.dataset.stepIndex = stepIdx;
            });

            // Обновляем ссылки шага
            step.querySelectorAll('.link').forEach((link, linkIdx) => {
                link.querySelectorAll('input').forEach(input => {
                    input.name = input.name
                        .replace(/steps-\d+-links-\d+/, `steps-${stepIdx}-links-${linkIdx}`);
                });
            });
        });

        // Обновление ссылок рецепта
        document.querySelectorAll('#all_links .link').forEach((link, linkIdx) => {
            link.querySelectorAll('input').forEach(input => {
                input.name = input.name.replace(/links-\d+/, `links-${linkIdx}`);
            });
        });
    }

    static async addInitialElements() {
        const ingredientsContainer = document.getElementById('cont_ing');
        if (ingredientsContainer && ingredientsContainer.children.length === 0) {
            await this.addIngredient(ingredientsContainer, 0);
        }

        const stepsContainer = document.getElementById('cont_steps');
        if (stepsContainer && stepsContainer.querySelectorAll('.steps__elem').length === 0) {
            await this.addStep(stepsContainer, 0);
        }

        const recipeLinksContainer = document.getElementById('all_links');
        if (recipeLinksContainer && recipeLinksContainer.children.length === 0) {
            await this.addRecipeLink(0);
        }
    }

    static initAddButtons() {
        // Кнопка добавления ингредиента
        document.getElementById('add_ingredient')?.addEventListener('click', async () => {
            const container = document.getElementById('cont_ing');
            const index = container.querySelectorAll('.ingredient').length;
            await this.addIngredient(container, index);
        });

        // Кнопка добавления шага
        document.getElementById('add_step')?.addEventListener('click', async () => {
            const container = document.getElementById('cont_steps');
            const index = container.querySelectorAll('.steps__elem').length;
            await this.addStep(container, index);
        });
    }

    static initFormSubmit() {
        const form = document.querySelector('form');
        if (!form) return;

        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            // Очистка предыдущих ошибок
            this.clearFormErrors();
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('error-field');
                    isValid = false;
                } else {
                    field.classList.remove('error-field');
                }
            });

            if (!isValid) {
                this.showFormErrors({
                    'form_error': ['Пожалуйста, заполните все обязательные поля']
                });
                return;
            }

            const submitButton = form.querySelector('button[type="submit"]');
            const loadingWave = document.getElementById('loading-wave');

            try {
                // Показать загрузку
                if (submitButton) submitButton.disabled = true;
                if (loadingWave) loadingWave.style.display = 'flex';

                const formData = new FormData(form);
                console.log(Array.from(formData.keys()));
                console.log(Array.from(formData.values()));
                for (let element of formData) {
                    console.log(element)
                }

                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('input[name="csrf_token"]')?.value || '',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json'
                    }
                });

                const result = await response.json();

                if (!response.ok) {
                    if (result.errors) {
                        this.showFormErrors(result.errors);
                    } else {
                        throw new Error(result.message || 'Ошибка сервера');
                    }
                    return;
                }

                // Успешная отправка
                if (result.redirect) {
                    window.location.href = result.redirect;
                }

            } catch (error) {
                console.error('Ошибка:', error);
                this.showFormErrors({
                    'form_error': [error.message || 'Ошибка при отправке формы']
                });
            } finally {
                if (submitButton) submitButton.disabled = false;
                if (loadingWave) loadingWave.style.display = 'none';
            }
        }.bind(this));
    }

    static clearFormErrors() {
        const errorContainer = document.getElementById('form-errors');
        const errorList = document.getElementById('error-list');

        if (errorContainer) errorContainer.style.display = 'none';
        if (errorList) errorList.innerHTML = '';

        document.querySelectorAll('.error-field').forEach(el => {
            el.classList.remove('error-field');
        });

        document.querySelectorAll('.error-message').forEach(el => {
            el.remove();
        });
    }


    static showFormErrors(errors) {
        const errorContainer = document.getElementById('form-errors');
        const errorList = document.getElementById('error-list');

        if (!errorContainer || !errorList) {
            console.error('Контейнеры ошибок не найдены');
            return;
        }

        this.clearFormErrors();

        errorContainer.style.display = 'block';
        errorList.innerHTML = '';

        // Сначала показываем общие ошибки формы
        if (errors.form_error) {
            errors.form_error.forEach(error => {
                const li = document.createElement('li');
                li.textContent = error;
                errorList.appendChild(li);
            });
        }

        // Затем показываем ошибки полей
        for (const fieldName in errors) {
            if (fieldName === 'form_error') continue;

            const fieldErrors = errors[fieldName];
            const field = this.findFormField(fieldName);

            if (field) {
                field.classList.add('error-field');

                // Создаем элемент с ошибкой
                const errorElement = document.createElement('div');
                errorElement.className = 'error-message';
                errorElement.textContent = fieldErrors.join(', ');

                // Добавляем после поля
                field.parentNode.appendChild(errorElement);
            }
        }

        errorContainer.scrollIntoView({behavior: 'smooth'});
    }

    static getFieldLabel(fieldName) {
        // Маппинг технических имен полей на человекочитаемые
        const labels = {
            'name': 'Название',
            'theme': 'Тема',
            'description': 'Описание',
            'hashtags': 'Хэштеги',
            'ingredients': 'Ингредиенты',
            'steps': 'Шаги',
            'result': 'Результат',
            'form_error': 'Ошибка формы'
        };

        return labels[fieldName] || fieldName;
    }

    static findFormField(fieldName) {
        // Ищем поле по точному совпадению имени
        let field = document.querySelector(`[name="${fieldName}"]`);

        // Если не нашли, пробуем найти по частичному совпадению (для динамически добавленных полей)
        if (!field) {
            const parts = fieldName.split('-');
            if (parts[0] === 'ingredients') {
                const index = parts[1];
                const fieldName = parts[2];
                field = document.querySelector(`[name="ingredients-${index}-${fieldName}"]`);
            } else if (parts[0] === 'steps') {
                const index = parts[1];
                const fieldName = parts[2];
                field = document.querySelector(`[name="steps-${index}-${fieldName}"]`);
            }
        }

        return field;
    }

    static async init() {
        await this.addInitialElements();
        this.initAddButtons();
        this.initDeleteHandlers();
        this.initImageHandlers();
        this.initRecipeLinkHandlers();
        this.initFormSubmit();

        document.addEventListener('click', async (e) => {
            if (e.target.classList.contains('add--step_link__button')) {
                const stepElement = e.target.closest('.steps__elem');
                if (stepElement) {
                    const stepIndex = this.getStepIndex(stepElement);
                    const linkCount = stepElement.querySelectorAll('.link').length;
                    await this.addStepLink(stepIndex, linkCount);
                }
            }
        });
    }
}
