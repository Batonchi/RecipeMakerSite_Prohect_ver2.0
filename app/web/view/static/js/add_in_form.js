class Patterns {
    static step = `
        <div class="steps__elem">
            <div class="block--flex_row">
                <div class="block--flex_column">
                    <div class="grid_input_custom_label var_grid_1">
                        <div class="label_back border_bottom_right_top_left">имя</div>
                        <input type="text"
                               name="steps-__index__-name"
                               class="border_bottom style_font limit_width_input"
                               required>
                        <div class="border_bottom label_back">номер</div>
                        <input type="text"
                               name="steps-__index__-number"
                               class="style_font border_top_right_bottom_left limit_width_input"
                               required>
                    </div>
                    <div class="grid_input_custom_label var_grid_2">
                        <div class="label_back border_right">описание</div>
                        <textarea name="steps-__index__-description"
                                  class="style_font border_left"
                                  required
                                  style="resize: none; border: none"></textarea>
                        <div class="label_back border_top_right_bottom_left">пояснение</div>
                        <textarea name="steps-__index__-explanations"
                                  class="style_font border_bottom_right_top_left"
                                  required
                                  style="resize: none; border: none"></textarea>
                    </div>
                    <div class="step--add_graphic border_top border_bottom">
                        <div class="border_bottom border_top container">
                            выберите графическую составляющую этапа
                            <div id="container_graph-__index__"></div>
                        </div>
                        <button class="border_bottom button--add_images" type="button" data-step-index="__index__">+</button>
                    </div>
                    <div class="step--add_links links--add border_bottom border_top">
                        <div class="container border_bottom border_top" id="step_links-__index__">
                            <div class="link">
                                <input type="text"
                                       name="steps-__index__-links-0-link_description"
                                       placeholder="куда ведет"
                                       class="where border_bottom border_top"
                                       required>
                                <input type="text"
                                       name="steps-__index__-links-0-link"
                                       placeholder="ссылка"
                                       class="link_str border_bottom border_top"
                                       required>
                                <label class="label__button--delete_link">x</label>
                            </div>
                        </div>
                        <div class="between_link_and_add border_bottom border_top">
                            нажмите +, чтобы добавить ссылку
                        </div>
                        <button class="add-link-button border_bottom" type="button" data-step-index="__index__">+</button>
                    </div>
                </div>
                <button class="step__elem--del" type="button">x</button>
            </div>
        </div>
    `;

    static ingredient = `
        <div class="ingredient block--flex_row">
            <label class="id_ing">__display_index__</label>
            <input type="text" 
                   name="ingredients-__index__-name" 
                   class="style_font" 
                   placeholder="наименование"
                   required>
            <input type="text" 
                   name="ingredients-__index__-for_what" 
                   class="style_font" 
                   placeholder="для чего">
            <input type="number" 
                   name="ingredients-__index__-quantity" 
                   class="style_font" 
                   placeholder="кол-во"
                   required>
            <label class="label__button--delete_ing">x</label>
        </div>
    `;

    static link = `
        <div class="link">
            <input type="text"
                   name="steps-__step_index__-links-__link_index__-link_description"
                   placeholder="куда ведет"
                   class="where border_bottom border_top"
                   required>
            <input type="text"
                   name="steps-__step_index__-links-__link_index__-link"
                   placeholder="ссылка"
                   class="link_str border_bottom border_top"
                   required>
            <label class="label__button--delete_link">x</label>
        </div>
    `;
}

export class AddInForm {
    static async fetchTemplate(type, params = {}) {
        const url = new URL(`/form/get-${type}-form`, window.location.origin);
        Object.entries(params).forEach(([key, value]) => {
            url.searchParams.append(key, value);
        });

        const response = await fetch(url);
        return await response.text();
    }

    static async addStep(container, index) {
        const html = await this.fetchTemplate('step', { index });
        const div = document.createElement('div');
        div.innerHTML = html;
        container.appendChild(div);

        // Инициализация обработчиков для нового шага
        this.initStepHandlers(div.querySelector('.steps__elem'));
        return div;
    }

    static async addIngredient(container, index) {
        const html = await this.fetchTemplate('ingredient', { index });
        const div = document.createElement('div');
        div.innerHTML = html
            .replace(/__index__/g, index)
            .replace(/__display_index__/g, index + 1);
        container.appendChild(div);
        return div;
    }

    static async addLink(stepIndex, linkIndex) {
        const container = document.getElementById(`step_links-${stepIndex}`);
        if (!container) return;

        const html = await this.fetchTemplate('link', { step_index: stepIndex, link_index: linkIndex });
        const div = document.createElement('div');
        div.innerHTML = html;
        container.appendChild(div);
        return div;
    }

    static initStepHandlers(stepElement) {
        const stepIndex = this.getStepIndex(stepElement);

        // Обработчик добавления ссылок
        stepElement.querySelector('.add-link-button')?.addEventListener('click', () => {
            const linkCount = stepElement.querySelectorAll('.link').length;
            this.addLink(stepIndex, linkCount);
        });

        // Обработчик добавления изображений
        stepElement.querySelector('.button--add_images')?.addEventListener('click', function() {
            const stepIndex = this.getAttribute('data-step-index');
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';
            fileInput.multiple = true;
            fileInput.click();

            fileInput.addEventListener('change', function(e) {
                const files = e.target.files;
                const container = document.getElementById(`container_graph-${stepIndex}`);

                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const reader = new FileReader();

                    reader.onload = function(e) {
                        const imageDiv = document.createElement('div');
                        imageDiv.className = 'image-item';
                        imageDiv.style.display = 'flex';
                        imageDiv.style.flexDirection = 'column';
                        imageDiv.style.gap = '20px';
                        imageDiv.style.maxWidth = '830px';

                        const imgPreview = document.createElement('img');
                        imgPreview.src = e.target.result;
                        imgPreview.style.maxWidth = '100px';
                        imgPreview.style.maxHeight = '100px';

                        imageDiv.appendChild(imgPreview);
                        imageDiv.addEventListener('click', () => imageDiv.remove());

                        container.appendChild(imageDiv);
                    };
                    reader.readAsDataURL(file);
                }
            });
        });
    }

    static getStepIndex(stepElement) {
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
            ing.querySelector('.id_ing').textContent = idx + 1;
            ing.querySelectorAll('input').forEach(input => {
                input.name = input.name.replace(/ingredients-\d+/, `ingredients-${idx}`);
            });
        });

        // Обновление индексов шагов и их ссылок
        document.querySelectorAll('.steps__elem').forEach((step, stepIdx) => {
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
                        .replace(/steps-\d+/, `steps-${stepIdx}`)
                        .replace(/links-\d+/, `links-${linkIdx}`);
                });
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

export class AddInForm {
    constructor(container, patternType, index) {
        this.container = container;
        this.patternType = patternType;
        this.index = index;
    }

    static getPattern(patternType) {
        switch (patternType) {
            case 'step': return Patterns.step;
            case 'ingredient': return Patterns.ingredient;
            case 'link': return Patterns.link;
            default: return '';
        }
    }

    addToContainer() {
        let pattern = AddInForm.getPattern(this.patternType);
        pattern = pattern.replace(/__name__/g, this.index);
        pattern = pattern.replace(/__index__/g, this.index + 1);

        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = pattern;
        //
        // alert(this.container.className)
        this.container.appendChild(tempDiv);
        return tempDiv;
    }

    static addInitialElements() {
        // Добавляем первый ингредиент
        const ingredientsContainer = document.getElementById('cont_ing');
        if (ingredientsContainer && ingredientsContainer.children.length === 0) {
            new AddInForm(ingredientsContainer, 'ingredient', 0).addToContainer();
        }

        // Добавляем первый шаг
        const stepsContainer = document.querySelector('.steps .block--flex_column');
        if (stepsContainer && stepsContainer.querySelectorAll('.steps__elem').length === 0) {
            new AddInForm(stepsContainer, 'step', 0).addToContainer();
        }
    }
}

// Инициализация формы при загрузке
document.addEventListener('DOMContentLoaded', () => {
    AddInForm.addInitialElements();

    // Обработчики для кнопок добавления
    document.querySelector('.plus_ing').addEventListener('click', () => {
        const container = document.getElementById('cont_ing');
        const index = container.children.length;
        new AddInForm(container, 'ingredient', index).addToContainer();
    });

    document.querySelectorAll('.add-button').forEach(button => {
        button.addEventListener('click', function() {
            const container = this.closest('.block--flex_column')?.querySelector('.container') ||
                            this.closest('.step--add_links')?.querySelector('.container');
            if (container) {
                const index = container.querySelectorAll('.steps__elem').length ||
                              container.querySelectorAll('input[type="text"]').length / 2;
                new AddInForm(container,
                    this.closest('.step--add_links') ? 'link' : 'step',
                    index).addToContainer();
            }
        });
    });

    document.querySelector('.button--add_images').addEventListener('click', function() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.multiple = true;

    fileInput.click();

    fileInput.addEventListener('change', function(e) {
        const files = e.target.files;
        const container = document.getElementById('container_graph');
        for (let i = 0; i < files.length; i++) {
            const file = files[i];

            const reader = new FileReader();

            reader.onload = function(e) {
                const imageDiv = document.createElement('div');
                imageDiv.className = 'image-item';
                imageDiv.style.display = 'flex'
                imageDiv.style.flexDirection = 'column'
                imageDiv.style.gap = '20px'
                imageDiv.style.maxWidth = '830px'
                const imgPreview = document.createElement('img');
                imgPreview.src = e.target.result;
                imgPreview.style.maxWidth = '100px';
                imgPreview.style.maxHeight = '100px';
                imageDiv.appendChild(imgPreview);
                imageDiv.addEventListener('click', (event) => {
                    event.target.remove(this)
                })
                container.appendChild(imageDiv);
            };
            reader.readAsDataURL(file);
        }
    });
});
    // Обработчики для удаления
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('step__elem--del')) {
            e.target.closest('.steps__elem').remove();
        }
        if (e.target.classList.contains('label__button--delete_ing')) {
            e.target.closest('.ingredient').remove();
        }
        if (e.target.classList.contains('label__button--delete_link)')) {
            e.target.closest('')
        }
    });
});