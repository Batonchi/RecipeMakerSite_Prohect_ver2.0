class RecipeForm {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 6;
        this.zoomLevel = 1;
        this.baseFontSize = 16ё;
        this.recipeData = null;
        this.selectedBlock = null;
        this.blocks = [];
        this.previewWrapper = document.getElementById('previewWrapper');
        this.init();
    }

    init() {
        this.loadRecipeData();
        this.initEventListeners();
        this.initColorPalettes();
        this.renderPreview();
        this.showStep(1);
    }

    loadRecipeData() {
        this.recipeData = {
            name: "Delicious Recipe",
            theme: "A wonderful dish for any occasion",
            description: "This recipe has been passed down for generations and is perfect for family gatherings.",
            hashtags: ["food", "recipe", "delicious"],
            categories: "Main Dish, Dinner",
            ingredients: [
                {name: "Flour", quantity: "2 cups"},
                {name: "Sugar", quantity: "1 cup"},
                {name: "Eggs", quantity: "3"},
                {name: "Milk", quantity: "1 cup"}
            ],
            steps: [
                {number: 1, name: "Mix dry ingredients"},
                {number: 2, name: "Add wet ingredients"},
                {number: 3, name: "Bake at 350°F for 30 minutes"}
            ],
            result: "A delicious cake that everyone will love!",
            result_link: "#",
            result_link_description: "See more recipes"
        };
    }

    initEventListeners() {
        document.getElementById('savePngBtn').addEventListener('click', () => this.saveAsPng());
        document.getElementById('prevStepBtn').addEventListener('click', () => this.prevStep());
        document.getElementById('nextStepBtn').addEventListener('click', () => this.nextStep());
        document.querySelectorAll('.step-dot').forEach(dot => {
            dot.addEventListener('click', () => {
                const step = parseInt(dot.dataset.step);
                this.showStep(step);
            });
        });
        document.getElementById('zoomInBtn').addEventListener('click', () => this.zoomIn());
        document.getElementById('zoomOutBtn').addEventListener('click', () => this.zoomOut());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearAll());
        document.querySelectorAll('.block-type').forEach(block => {
            block.addEventListener('click', () => {
                const type = block.dataset.type;
                this.addBlock(type);
            });
        });
        document.querySelectorAll('.layout-option').forEach(option => {
            option.addEventListener('click', () => {
                const layout = option.dataset.layout;
                this.applyLayout(layout);
            });
        });
        document.getElementById('fontFamily').addEventListener('change', () => this.updateTextSettings());
        document.getElementById('fontSize').addEventListener('input', (e) => {
            document.getElementById('fontSizeValue').textContent = e.target.value + 'px';
            this.updateTextSettings();
        });
        document.getElementById('fontWeight').addEventListener('change', () => this.updateTextSettings());
        document.getElementById('italicCheckbox').addEventListener('change', () => this.updateTextSettings());
        document.getElementById('underlineCheckbox').addEventListener('change', () => this.updateTextSettings());
        document.querySelectorAll('.resolution-option').forEach(option => {
            option.addEventListener('click', () => {
                const resolution = option.dataset.resolution;
                this.setResolution(resolution);
            });
        });

        document.querySelectorAll('.background-option').forEach(option => {
            option.addEventListener('click', () => {
                const bg = option.dataset.bg;
                this.setBackground(bg);
            });
        });
        document.getElementById('saveHtmlBtn').addEventListener('click', () => this.saveAsHtml());
        document.getElementById('savePngBtn').addEventListener('click', () => this.saveAsPng());
        document.addEventListener('contextmenu', (e) => {
            if (e.target.closest('.block')) {
                e.preventDefault();
                this.showContextMenu(e, e.target.closest('.block'));
            }
        });

        document.addEventListener('click', () => this.hideContextMenu());
        document.getElementById('fontColor').addEventListener('input', (e) => {
            this.updateTextSettings();
        });
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('palette-color')) {
                this.editPaletteColor(e.target);
            }
        });
    }

    initColorPalettes() {
        const palettesContainer = document.getElementById('colorPalettes');
        palettesContainer.innerHTML = '';

        // Purple palettes
        const purplePalettes = [
            {name: "Classic Purple", colors: ["#2D3250", "#3D4468", "#545B81", "#686F95", "#8F94B4"]},
            {name: "Deep Purple", colors: ["#1A1C2E", "#2D3250", "#4A4F7A", "#686F95", "#A0A5C8"]},
            {name: "Pastel Purple", colors: ["#D1D4E4", "#B8BCE0", "#9FA5DB", "#868ED6", "#6D77D1"]}
        ];

        // Additional palettes
        const additionalPalettes = [
            {name: "Autumn", colors: ["#4A2511", "#8D3B1B", "#C45D2B", "#E88B4F", "#F2B279"]},
            {name: "Ocean", colors: ["#0A2463", "#3E5C76", "#7EA8BE", "#BFD7EA", "#F2F2F2"]},
            {name: "Forest", colors: ["#283618", "#4A5D23", "#606C38", "#A5AE8F", "#D4D8C9"]},
            {name: "Sunset", colors: ["#370617", "#6A040F", "#9D0208", "#D00000", "#DC2F02"]},
            {name: "Mint", colors: ["#0B3C49", "#16697A", "#379683", "#57C4B0", "#87E0D1"]},
            {name: "Berry", colors: ["#3A0CA3", "#480CA8", "#560BAD", "#7209B7", "#B5179E"]},
            {name: "Earth", colors: ["#3A3335", "#5C4742", "#7D5E5A", "#9D7879", "#C69F9F"]},
            {name: "Sky", colors: ["#012A4A", "#013A63", "#01497C", "#014F86", "#2A6F97"]},
            {name: "Warm", colors: ["#582F0E", "#7F4F24", "#936639", "#A68A64", "#B6AD90"]},
            {name: "Cool", colors: ["#0D1B2A", "#1B263B", "#415A77", "#778DA9", "#E0E1DD"]}
        ];

        // Create palette elements
        [...purplePalettes, ...additionalPalettes].forEach((palette, index) => {
            const paletteElement = document.createElement('div');
            paletteElement.className = 'palette-option';
            paletteElement.dataset.palette = index;

            const colorsElement = document.createElement('div');
            colorsElement.className = 'palette-colors';

            palette.colors.forEach(color => {
                const colorElement = document.createElement('div');
                colorElement.className = 'palette-color';
                colorElement.style.backgroundColor = color;
                colorsElement.appendChild(colorElement);
            });

            const nameElement = document.createElement('div');
            nameElement.textContent = palette.name;

            paletteElement.appendChild(colorsElement);
            paletteElement.appendChild(nameElement);

            paletteElement.addEventListener('click', () => {
                this.applyColorPalette(palette.colors);
            });

            palettesContainer.appendChild(paletteElement);
        });

        // Palette creator
        const paletteCreator = document.createElement('div');
        paletteCreator.className = 'palette-creator';
        paletteCreator.innerHTML = `
            <h3>Create Custom Palette</h3>
            <div class="palette-creator-colors">
                <div class="palette-creator-color"><input type="color" value="#545B81"></div>
                <div class="palette-creator-color"><input type="color" value="#686F95"></div>
                <div class="palette-creator-color"><input type="color" value="#8F94B4"></div>
                <div class="palette-creator-color"><input type="color" value="#D1D4E4"></div>
            </div>
            <input type="text" id="paletteName" placeholder="Palette name" class="form-input">
            <button class="control-btn" id="createPaletteBtn">Create Palette</button>
        `;

        palettesContainer.appendChild(paletteCreator);

        document.getElementById('createPaletteBtn').addEventListener('click', () => {
            const colors = Array.from(document.querySelectorAll('.palette-creator-color input')).map(input => input.value);
            const name = document.getElementById('paletteName').value || 'Custom Palette';

            if (colors.length > 0) {
                this.applyColorPalette(colors);

                // Add new palette to the list
                const paletteElement = document.createElement('div');
                paletteElement.className = 'palette-option';

                const colorsElement = document.createElement('div');
                colorsElement.className = 'palette-colors';

                colors.forEach(color => {
                    const colorElement = document.createElement('div');
                    colorElement.className = 'palette-color';
                    colorElement.style.backgroundColor = color;
                    colorsElement.appendChild(colorElement);
                });

                const nameElement = document.createElement('div');
                nameElement.textContent = name;

                paletteElement.appendChild(colorsElement);
                paletteElement.appendChild(nameElement);

                paletteElement.addEventListener('click', () => {
                    this.applyColorPalette(colors);
                });

                palettesContainer.insertBefore(paletteElement, paletteCreator);
            }
        });
    }

    showStep(step) {
        this.currentStep = Math.max(1, Math.min(step, this.totalSteps));

        document.querySelectorAll('.step-dot').forEach((dot, index) => {
            dot.classList.toggle('active', index + 1 <= this.currentStep);
        });

        document.getElementById('prevStepBtn').disabled = this.currentStep === 1;
        document.getElementById('nextStepBtn').disabled = this.currentStep === this.totalSteps;
        document.getElementById('saveOptions').style.display = this.currentStep === this.totalSteps ? 'flex' : 'none';

        document.querySelectorAll('.step-content').forEach(content => {
            content.classList.remove('active');
        });

        document.querySelector(`.step-content[data-step="${this.currentStep}"]`).classList.add('active');
    }

    nextStep() {
        this.showStep(this.currentStep + 1);
    }

    prevStep() {
        this.showStep(this.currentStep - 1);
    }

    zoomIn() {
        this.zoomLevel = Math.min(2, this.zoomLevel + 0.1);
        this.updateZoom();
    }

    zoomOut() {
        this.zoomLevel = Math.max(0.5, this.zoomLevel - 0.1);
        this.updateZoom();
    }

    updateZoom() {
        this.previewWrapper.style.transform = `scale(${this.zoomLevel})`;
    }

    renderPreview() {
        this.previewWrapper.innerHTML = '';

        // Main card
        const mainCard = this.createMainCard();
        this.positionBlock(mainCard,
            this.previewWrapper.offsetWidth / 2 - mainCard.offsetWidth / 2,
            this.previewWrapper.offsetHeight / 2 - mainCard.offsetHeight / 2,
            0
        );

        // Standard blocks
        const blocks = [
            {
                type: 'description',
                title: 'Description',
                content: this.recipeData.description,
                x: 50,
                y: 50,
                rotation: -5
            },
            {
                type: 'hashtags',
                title: 'Hashtags',
                content: this.recipeData.hashtags.join(' '),
                x: 360,
                y: 30,
                rotation: -2
            },
            {type: 'categories', title: 'Categories', content: this.recipeData.categories, x: 670, y: 50, rotation: 5},
            {
                type: 'ingredients',
                title: 'Ingredients',
                content: this.createIngredientsContent(),
                x: 50,
                y: 570,
                rotation: 5
            },
            {type: 'steps', title: 'Steps', content: this.createStepsContent(), x: 360, y: 590, rotation: 2},
            {type: 'result', title: 'Result', content: this.recipeData.result, x: 670, y: 570, rotation: -5}
        ];

        blocks.forEach(blockData => {
            const block = this.createBlock(blockData.type, blockData.title, blockData.content);
            this.positionBlock(block, blockData.x, blockData.y, blockData.rotation);

            this.blocks.push({
                element: block,
                type: blockData.type,
                editable: false,
                removable: false
            });
        });

        this.makeBlocksDraggable();
    }

    createMainCard() {
        const card = document.createElement('div');
        card.className = 'block main-card';
        card.dataset.id = 'main-card';

        card.innerHTML = `
            <div class="block-header">
                <h1 class="recipe-title" contenteditable="true">${this.recipeData.name}</h1>
                <input type="color" class="color-picker" value="#545B81">
            </div>
            <p class="recipe-theme" contenteditable="true">${this.recipeData.theme}</p>
            <h3 contenteditable="true">Ingredients:</h3>
            <div class="block-content-editable" contenteditable="true">${this.createIngredientsContent()}</div>
        `;

        // Color picker
        card.querySelector('.color-picker').addEventListener('input', (e) => {
            card.style.borderColor = e.target.value;
        });

        // Make draggable
        this.makeBlockDraggable(card);

        // Add to blocks array
        this.blocks.push({
            element: card,
            type: 'main',
            editable: true,
            removable: false
        });

        return card;
    }

    showContextMenu(e, block) {
        e.preventDefault();

        const blockData = this.blocks.find(b => b.element === block);
        if (!blockData) return;

        this.selectedBlock = block;

        const menu = document.getElementById('contextMenu');
        menu.innerHTML = `
            <div class="context-menu-item" data-action="edit">Edit Block</div>
            ${blockData.removable ? '<div class="context-menu-item" data-action="delete">Delete Block</div>' : ''}
            <div class="context-menu-item" data-action="color">Change Color</div>
            <div class="context-menu-item" data-action="rotate">Rotate</div>
            <div class="context-menu-item" data-action="radius">Corner Radius</div>
            <div class="context-menu-item" data-action="bring-forward">Bring Forward</div>
            <div class="context-menu-item" data-action="send-backward">Send Backward</div>
            <div class="context-menu-item" data-action="properties">Properties</div>
            ${blockData.type === 'main' ? '<div class="context-menu-item" data-action="edit-content">Edit Content</div>' : ''}
        `;

        menu.style.display = 'block';
        menu.style.left = e.clientX + 'px';
        menu.style.top = e.clientY + 'px';

        menu.querySelectorAll('.context-menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                this.handleContextMenuAction(item.dataset.action);
            });
        });
    }

    handleContextMenuAction(action) {
        if (!this.selectedBlock) return;

        const blockData = this.blocks.find(b => b.element === this.selectedBlock);

        switch (action) {
            case 'edit':
                this.editBlock(this.selectedBlock);
                break;
            case 'delete':
                this.deleteBlock(this.selectedBlock);
                break;
            case 'color':
                this.changeBlockColor(this.selectedBlock);
                break;
            case 'rotate':
                this.rotateBlock(this.selectedBlock);
                break;
            case 'radius':
                this.changeCornerRadius(this.selectedBlock);
                break;
            case 'bring-forward':
                this.bringForward(this.selectedBlock);
                break;
            case 'send-backward':
                this.sendBackward(this.selectedBlock);
                break;
            case 'properties':
                this.showPropertiesEditor(this.selectedBlock);
                break;
            case 'edit-content':
                this.editMainBlockContent(this.selectedBlock);
                break;
        }

        this.hideContextMenu();
    }

    editMainBlockContent(block) {
        // Create editor overlay
        const editor = document.createElement('div');
        editor.className = 'main-block-editor';

        // Get current content
        const title = block.querySelector('.recipe-title').textContent;
        const theme = block.querySelector('.recipe-theme').textContent;
        const ingredientsTitle = block.querySelector('h3').textContent;
        const ingredientsContent = block.querySelector('.block-content-editable').innerHTML;

        // Create editor form
        editor.innerHTML = `
            <div class="editor-form">
                <h2>Edit Main Block</h2>
                <div class="form-group">
                    <label>Recipe Title:</label>
                    <input type="text" id="editTitle" value="${title}">
                </div>
                <div class="form-group">
                    <label>Recipe Theme:</label>
                    <textarea id="editTheme">${theme}</textarea>
                </div>
                <div class="form-group">
                    <label>Ingredients Title:</label>
                    <input type="text" id="editIngredientsTitle" value="${ingredientsTitle}">
                </div>
                <div class="form-group">
                    <label>Ingredients:</label>
                    <div class="ingredients-editor" id="editIngredientsContent" contenteditable="true">${ingredientsContent}</div>
                </div>
                <div class="editor-buttons">
                    <button class="control-btn" id="saveMainBlock">Save</button>
                    <button class="control-btn" id="cancelMainBlock">Cancel</button>
                </div>
            </div>
        `;

        document.body.appendChild(editor);

        // Save handler
        document.getElementById('saveMainBlock').addEventListener('click', () => {
            block.querySelector('.recipe-title').textContent = document.getElementById('editTitle').value;
            block.querySelector('.recipe-theme').textContent = document.getElementById('editTheme').value;
            block.querySelector('h3').textContent = document.getElementById('editIngredientsTitle').value;
            block.querySelector('.block-content-editable').innerHTML = document.getElementById('editIngredientsContent').innerHTML;
            editor.remove();
        });

        // Cancel handler
        document.getElementById('cancelMainBlock').addEventListener('click', () => {
            editor.remove();
        });

        // Close editor when clicking outside
        editor.addEventListener('click', (e) => {
            if (e.target === editor) {
                editor.remove();
            }
        });
    }

    makeBlockDraggable(block) {
        let isDragging = false;
        let offsetX, offsetY;

        block.addEventListener('mousedown', (e) => {
            if (e.button !== 0) return; // Only left click

            isDragging = true;
            offsetX = e.clientX - block.getBoundingClientRect().left;
            offsetY = e.clientY - block.getBoundingClientRect().top;

            block.style.cursor = 'grabbing';
            block.style.zIndex = '1000';

            e.stopPropagation();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;

            const container = this.previewWrapper.getBoundingClientRect();

            let x = e.clientX - container.left - offsetX;
            let y = e.clientY - container.top - offsetY;

            // Boundary checks
            x = Math.max(0, Math.min(x, container.width - block.offsetWidth));
            y = Math.max(0, Math.min(y, container.height - block.offsetHeight));

            block.style.left = x + 'px';
            block.style.top = y + 'px';
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                block.style.cursor = 'move';
                block.style.zIndex = '10';
            }
        });

        // Enable right-click for context menu
        block.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            this.showContextMenu(e, block);
        });
    }

    createBlock(id, title, content) {
        const block = document.createElement('div');
        block.className = 'block';
        block.dataset.id = id;

        block.innerHTML = `
            <div class="block-header">
                <h3>${title}</h3>
                <input type="color" class="color-picker" value="#686F95">
            </div>
            <div class="block-content-editable" contenteditable="true">${content}</div>
        `;

        // Color picker
        block.querySelector('.color-picker').addEventListener('input', (e) => {
            block.style.backgroundColor = e.target.value;
        });

        // Highlight on hover
        block.addEventListener('mouseenter', () => {
            block.style.boxShadow = '0 0 0 2px rgba(0,0,0,0.3)';
        });

        block.addEventListener('mouseleave', () => {
            block.style.boxShadow = '';
        });

        return block;
    }

    createIngredientsContent() {
        return this.recipeData.ingredients.map(ing =>
            `<div>${ing.name} - ${ing.quantity}</div>`
        ).join('');
    }

    createStepsContent() {
        return this.recipeData.steps.map(step =>
            `<div>${step.number}. ${step.name}</div>`
        ).join('');
    }

    positionBlock(block, x, y, rotation) {
        block.style.position = 'absolute';
        block.style.left = `${x}px`;
        block.style.top = `${y}px`;
        block.style.transform = `rotate(${rotation}deg)`;
        this.previewWrapper.appendChild(block);
    }

    addBlock(type) {
        let block;
        let id = `custom-${Date.now()}`;
        let title = 'Custom Block';
        let content = 'Edit this content';

        switch (type) {
            case 'text':
                title = 'Text Block';
                content = 'Double click to edit this text';
                break;
            case 'image':
                title = 'Image Block';
                content = '<div style="text-align:center;padding:20px;"><input type="file" accept="image/*" style="display:none;" id="image-upload"><label for="image-upload" style="cursor:pointer;">Click to upload image</label></div>';
                break;
            case 'ingredients':
                title = 'Ingredients';
                content = this.createIngredientsContent();
                break;
            case 'steps':
                title = 'Steps';
                content = this.createStepsContent();
                break;
            case 'timer':
                title = 'Timer';
                content = '<div style="text-align:center;font-size:24px;">00:00</div><button style="display:block;margin:0 auto;">Start Timer</button>';
                break;
            case 'note':
                title = 'Note';
                content = 'Double click to edit this note';
                break;
            case 'quote':
                title = 'Quote';
                content = '"Double click to edit this quote"';
                break;
            case 'warning':
                title = 'Warning';
                content = 'Important! Double click to edit';
                break;
            case 'tip':
                title = 'Tip';
                content = 'Pro tip: Double click to edit';
                break;
            case 'nutrition':
                title = 'Nutrition';
                content = 'Calories: 0<br>Protein: 0g<br>Carbs: 0g<br>Fat: 0g';
                break;
            case 'equipment':
                title = 'Equipment';
                content = '- List your equipment here';
                break;
            case 'serving':
                title = 'Serving Suggestion';
                content = 'Suggest how to serve this dish';
                break;
            case 'video':
                title = 'Video';
                content = '<div style="text-align:center;padding:20px;"><input type="file" accept="video/*" style="display:none;" id="video-upload"><label for="video-upload" style="cursor:pointer;">Click to upload video</label></div>';
                break;
            case 'audio':
                title = 'Audio Note';
                content = '<div style="text-align:center;padding:20px;"><input type="file" accept="audio/*" style="display:none;" id="audio-upload"><label for="audio-upload" style="cursor:pointer;">Click to upload audio</label></div>';
                break;
            case 'rating':
                title = 'Rating';
                content = '<div style="text-align:center;">★★★★★</div>';
                break;
            case 'timer2':
                title = 'Countdown Timer';
                content = '<div style="text-align:center;font-size:24px;">30:00</div><button style="display:block;margin:0 auto;">Start Countdown</button>';
                break;
            case 'temperature':
                title = 'Temperature';
                content = '<div style="text-align:center;font-size:24px;">350°F</div>';
                break;
        }

        block = this.createBlock(id, title, content);

        // Position near center
        const x = this.previewWrapper.offsetWidth / 2 + (Math.random() * 200 - 100);
        const y = this.previewWrapper.offsetHeight / 2 + (Math.random() * 200 - 100);
        const rotation = -15 + Math.random() * 30;

        this.positionBlock(block, x, y, rotation);

        // Image upload handler
        if (type === 'image') {
            const input = block.querySelector('input');
            input.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (event) => {
                        block.querySelector('label').innerHTML = `<img src="${event.target.result}" style="max-width:100%;max-height:200px;">`;
                    };
                    reader.readAsDataURL(file);
                }
            });
        }

        // Add to blocks array
        this.blocks.push({
            element: block,
            type: type,
            editable: true,
            removable: true
        });

        // Make draggable
        this.makeBlockDraggable(block);
    }

    makeBlocksDraggable() {
        this.blocks.forEach(blockData => {
            this.makeBlockDraggable(blockData.element);
        });
    }

    applyLayout(layout) {
        const container = this.previewWrapper.getBoundingClientRect();
        const centerX = container.width / 2;
        const centerY = container.height / 2;
        const movableBlocks = this.blocks.filter(block => block.type !== 'main');

        movableBlocks.forEach((block, index) => {
            let x, y, rotation;

            switch (layout) {
                case 'circle':
                    const angle = (index / movableBlocks.length) * 2 * Math.PI;
                    const radius = Math.min(container.width, container.height) * 0.35;
                    x = centerX + Math.cos(angle) * radius - block.element.offsetWidth / 2;
                    y = centerY + Math.sin(angle) * radius - block.element.offsetHeight / 2;
                    rotation = (angle * 180 / Math.PI) % 360;
                    break;

                case 'grid':
                    const cols = Math.ceil(Math.sqrt(movableBlocks.length));
                    const cellWidth = container.width / (cols + 1);
                    const cellHeight = container.height / (cols + 1);

                    const col = index % cols;
                    const row = Math.floor(index / cols);

                    x = (col + 1) * cellWidth - block.element.offsetWidth / 2;
                    y = (row + 1) * cellHeight - block.element.offsetHeight / 2;
                    rotation = 0;
                    break;

                case 'spiral':
                    const spiralAngle = index * 0.5;
                    const spiralRadius = 50 + index * 20;
                    x = centerX + Math.cos(spiralAngle) * spiralRadius - block.element.offsetWidth / 2;
                    y = centerY + Math.sin(spiralAngle) * spiralRadius - block.element.offsetHeight / 2;
                    rotation = (spiralAngle * 180 / Math.PI) % 360;
                    break;

                case 'random':
                    x = Math.random() * (container.width - block.element.offsetWidth);
                    y = Math.random() * (container.height - block.element.offsetHeight);
                    rotation = -15 + Math.random() * 30;
                    break;

                case 'horizontal':
                    const hSpace = container.width / (movableBlocks.length + 1);
                    x = (index + 1) * hSpace - block.element.offsetWidth / 2;
                    y = centerY - block.element.offsetHeight / 2;
                    rotation = 0;
                    break;

                case 'vertical':
                    const vSpace = container.height / (movableBlocks.length + 1);
                    x = centerX - block.element.offsetWidth / 2;
                    y = (index + 1) * vSpace - block.element.offsetHeight / 2;
                    rotation = 0;
                    break;

                case 'grid-fit':
                    const gridCols = 3;
                    const gridRows = Math.ceil(movableBlocks.length / gridCols);
                    const gridCellW = container.width / gridCols;
                    const gridCellH = container.height / gridRows;

                    const gridCol = index % gridCols;
                    const gridRow = Math.floor(index / gridCols);

                    x = gridCol * gridCellW + (gridCellW - block.element.offsetWidth) / 2;
                    y = gridRow * gridCellH + (gridCellH - block.element.offsetHeight) / 2;
                    rotation = 0;
                    break;

                case 'diagonal':
                    const diagStep = Math.min(container.width, container.height) / (movableBlocks.length + 1);
                    x = index * diagStep;
                    y = index * diagStep;
                    rotation = 45;
                    break;

                case 'star':
                    const starAngle = (index / movableBlocks.length) * 2 * Math.PI;
                    const starRadius = index % 2 === 0 ?
                        Math.min(container.width, container.height) * 0.25 :
                        Math.min(container.width, container.height) * 0.4;
                    x = centerX + Math.cos(starAngle) * starRadius - block.element.offsetWidth / 2;
                    y = centerY + Math.sin(starAngle) * starRadius - block.element.offsetHeight / 2;
                    rotation = (starAngle * 180 / Math.PI) % 360;
                    break;

                case 'stretch':
                    // Stretch blocks to fill container
                    const stretchCols = Math.ceil(Math.sqrt(movableBlocks.length));
                    const stretchRows = Math.ceil(movableBlocks.length / stretchCols);
                    const stretchCellW = container.width / stretchCols;
                    const stretchCellH = container.height / stretchRows;

                    const stretchCol = index % stretchCols;
                    const stretchRow = Math.floor(index / stretchCols);

                    x = stretchCol * stretchCellW;
                    y = stretchRow * stretchCellH;
                    block.element.style.width = stretchCellW + 'px';
                    block.element.style.height = stretchCellH + 'px';
                    rotation = 0;
                    break;

                case 'masonry':
                    // Masonry layout
                    const masonryCols = 3;
                    const colHeights = new Array(masonryCols).fill(0);
                    const masonryCol = index % masonryCols;

                    x = masonryCol * (container.width / masonryCols);
                    y = colHeights[masonryCol];

                    // Update column height
                    colHeights[masonryCol] += block.element.offsetHeight;
                    rotation = 0;
                    break;

                case 'centered':
                    // All blocks centered together
                    x = centerX - block.element.offsetWidth / 2;
                    y = centerY - block.element.offsetHeight / 2;
                    rotation = 0;
                    break;

                case 'radial':
                    // Radial layout with text facing outward
                    const radialAngle = (index / movableBlocks.length) * 2 * Math.PI;
                    const radialRadius = Math.min(container.width, container.height) * 0.3;
                    x = centerX + Math.cos(radialAngle) * radialRadius - block.element.offsetWidth / 2;
                    y = centerY + Math.sin(radialAngle) * radialRadius - block.element.offsetHeight / 2;
                    rotation = (radialAngle * 180 / Math.PI + 90) % 360;
                    break;

                default:
                    return;
            }

            if (layout !== 'stretch') {
                block.element.style.width = '';
                block.element.style.height = '';
            }

            block.element.style.left = x + 'px';
            block.element.style.top = y + 'px';
            block.element.style.transform = `rotate(${rotation}deg)`;
        });
    }

    applyColorPalette(colors) {
        // Apply colors to elements
        const mainCard = this.blocks.find(block => block.type === 'main').element;
        mainCard.style.backgroundColor = colors[3] || '#f8f8f8';
        mainCard.style.borderColor = colors[0] || '#545B81';

        // Update color picker
        if (mainCard.querySelector('.color-picker')) {
            mainCard.querySelector('.color-picker').value = colors[0] || '#545B81';
        }

        // Apply to blocks
        this.blocks.forEach(block => {
            if (block.type !== 'main') {
                block.element.style.backgroundColor = colors[1] || '#686F95';
                block.element.style.borderColor = colors[0] || '#545B81';

                if (block.element.querySelector('.color-picker')) {
                    block.element.querySelector('.color-picker').value = colors[1] || '#686F95';
                }
            }
        });
    }

    updateTextSettings() {
        const fontFamily = document.getElementById('fontFamily').value;
        const fontSizePercent = document.getElementById('fontSize').value;
        const fontSize = (this.baseFontSize * fontSizePercent / 100) + 'px';
        const fontWeight = document.getElementById('fontWeight').value;
        const fontStyle = document.getElementById('italicCheckbox').checked ? 'italic' : 'normal';
        const textDecoration = document.getElementById('underlineCheckbox').checked ? 'underline' : 'none';
        const fontColor = document.getElementById('fontColor').value;

        document.getElementById('fontSizeValue').textContent = fontSizePercent + '%';

        this.previewWrapper.querySelectorAll('h1, h2, h3, p, li, div').forEach(text => {
            text.style.fontFamily = fontFamily;
            text.style.fontSize = fontSize;
            text.style.fontWeight = fontWeight;
            text.style.fontStyle = fontStyle;
            text.style.textDecoration = textDecoration;
            text.style.color = fontColor;
        });
    }

    editPaletteColor(colorElement) {
        // Создаем временный input для выбора цвета
        const colorInput = document.createElement('input');
        colorInput.type = 'color';
        colorInput.value = colorElement.style.backgroundColor || '#ffffff';

        // Позиционируем input поверх элемента цвета
        colorInput.style.position = 'absolute';
        colorInput.style.left = colorElement.getBoundingClientRect().left + 'px';
        colorInput.style.top = colorElement.getBoundingClientRect().top + 'px';
        colorInput.style.width = colorElement.offsetWidth + 'px';
        colorInput.style.height = colorElement.offsetHeight + 'px';
        colorInput.style.opacity = '0';
        colorInput.style.cursor = 'pointer';

        document.body.appendChild(colorInput);

        // Открываем палитру цветов
        colorInput.click();

        // Обработчик изменения цвета
        colorInput.addEventListener('input', (e) => {
            colorElement.style.backgroundColor = e.target.value;

            // Обновляем все блоки, использующие этот цвет
            this.updateBlocksWithPaletteColor();
        });

        // Удаляем input после выбора цвета
        colorInput.addEventListener('change', () => {
            document.body.removeChild(colorInput);
        });
    }

    updateBlocksWithPaletteColor() {
        // Здесь можно добавить логику обновления блоков при изменении цвета в палитре
        // Например, переприменить текущую палитру:
        const currentPalette = this.getCurrentPalette();
        if (currentPalette) {
            this.applyColorPalette(currentPalette);
        }
    }

    getCurrentPalette() {
        // Получаем текущие цвета из активной палитры
        const activePalette = document.querySelector('.palette-option.active');
        if (!activePalette) return null;

        const colors = [];
        activePalette.querySelectorAll('.palette-color').forEach(colorEl => {
            colors.push(colorEl.style.backgroundColor);
        });

        return colors;
    }

    setResolution(resolution) {
        if (resolution === 'custom') {
            const width = prompt('Enter width in pixels:', '1000');
            const height = prompt('Enter height in pixels:', '800');

            if (width && height) {
                this.previewWrapper.style.width = width + 'px';
                this.previewWrapper.style.height = height + 'px';
            }
            return;
        }

        const [width, height] = resolution.split('x').map(Number);
        this.previewWrapper.style.width = width + 'px';
        this.previewWrapper.style.height = height + 'px';
    }

    setBackground(bg) {
        if (bg === 'custom') {
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';
            fileInput.onchange = (e) => {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (event) => {
                        this.previewWrapper.style.backgroundImage = `url(${event.target.result})`;
                        this.previewWrapper.style.backgroundSize = 'cover';
                    };
                    reader.readAsDataURL(file);
                }
            };
            fileInput.click();
            return;
        }

        switch (bg) {
            case 'none':
                this.previewWrapper.style.background = 'white';
                this.previewWrapper.style.backgroundImage = 'none';
                break;
            case 'pattern1':
                this.previewWrapper.style.background = 'linear-gradient(45deg, #f0f0f0 25%, transparent 25%, transparent 75%, #f0f0f0 75%, #f0f0f0), linear-gradient(45deg, #f0f0f0 25%, transparent 25%, transparent 75%, #f0f0f0 75%, #f0f0f0)';
                this.previewWrapper.style.backgroundPosition = '0 0, 10px 10px';
                this.previewWrapper.style.backgroundSize = '20px 20px';
                break;
            case 'pattern2':
                this.previewWrapper.style.background = 'radial-gradient(circle, #f0f0f0 20%, transparent 20%)';
                this.previewWrapper.style.backgroundSize = '30px 30px';
                break;
        }
    }

    clearAll() {
        if (confirm('Are you sure you want to clear all custom blocks and reset to default?')) {
            this.blocks = this.blocks.filter(block => !block.removable);
            this.previewWrapper.querySelectorAll('.block').forEach(block => {
                if (block.classList.contains('main-card') ||
                    ['description', 'hashtags', 'categories', 'ingredients', 'steps', 'result']
                        .some(id => block.dataset.id === id)) return;

                block.remove();
            });

            // Reset to step 1
            this.showStep(1);
        }
    }


    hideContextMenu() {
        document.getElementById('contextMenu').style.display = 'none';
        this.selectedBlock = null;
    }

    editBlock(block) {
        const content = block.querySelector('.block-content-editable');
        if (content) {
            content.focus();
        }
    }

    deleteBlock(block) {
        if (confirm('Are you sure you want to delete this block?')) {
            this.blocks = this.blocks.filter(b => b.element !== block);
            block.remove();
        }
    }

    changeBlockColor(block) {
        const colorPicker = block.querySelector('.color-picker');
        if (colorPicker) {
            colorPicker.click();
        } else {
            const color = prompt('Enter a color (name, hex, rgb, etc.):', block.style.backgroundColor || '#686F95');
            if (color) {
                block.style.backgroundColor = color;
            }
        }
    }

    rotateBlock(block) {
        const currentRotation = block.style.transform.match(/rotate\(([-+]?\d+)deg\)/);
        const currentAngle = currentRotation ? parseInt(currentRotation[1]) : 0;
        const newAngle = prompt('Enter rotation angle (degrees):', currentAngle);

        if (newAngle !== null) {
            block.style.transform = `rotate(${newAngle}deg)`;
        }
    }

    changeCornerRadius(block) {
        const currentRadius = block.style.borderRadius || '0';
        const newRadius = prompt('Enter corner radius in pixels:', currentRadius.replace('px', ''));

        if (newRadius !== null) {
            block.style.borderRadius = `${newRadius}px`;
        }
    }

    bringForward(block) {
        block.style.zIndex = '100';
    }

    sendBackward(block) {
        block.style.zIndex = '1';
    }

    showPropertiesEditor(block) {
        const blockData = this.blocks.find(b => b.element === block);
        if (!blockData) return;

        const properties = `
            <div class="property-row">
                <label>Width:</label>
                <input type="number" id="propWidth" value="${block.offsetWidth}">
            </div>
            <div class="property-row">
                <label>Height:</label>
                <input type="number" id="propHeight" value="${block.offsetHeight}">
            </div>
            <div class="property-row">
                <label>Rotation:</label>
                <input type="number" id="propRotation" value="${this.getRotationAngle(block)}">
            </div>
            <div class="property-row">
                <label>Corner Radius:</label>
                <input type="number" id="propRadius" value="${parseInt(block.style.borderRadius) || 0}">
            </div>
            <div class="property-row">
                <label>Background Opacity:</label>
                <input type="range" id="propOpacity" min="0" max="1" step="0.1" value="${this.getBackgroundOpacity(block)}">
            </div>
            <button class="control-btn" id="applyProperties">Apply</button>
        `;

        const editor = document.createElement('div');
        editor.className = 'properties-editor';
        editor.innerHTML = `<h3>Block Properties</h3>${properties}`;

        document.body.appendChild(editor);

        // Position editor near the block
        const rect = block.getBoundingClientRect();
        editor.style.left = `${rect.right + 10}px`;
        editor.style.top = `${rect.top}px`;

        // Apply properties
        document.getElementById('applyProperties').addEventListener('click', () => {
            block.style.width = document.getElementById('propWidth').value + 'px';
            block.style.height = document.getElementById('propHeight').value + 'px';
            block.style.transform = `rotate(${document.getElementById('propRotation').value}deg)`;
            block.style.borderRadius = document.getElementById('propRadius').value + 'px';

            const opacity = document.getElementById('propOpacity').value;
            const bgColor = block.style.backgroundColor || '#686F95';
            block.style.backgroundColor = this.setOpacity(bgColor, opacity);

            editor.remove();
        });

        // Close editor when clicking outside
        document.addEventListener('click', (e) => {
            if (!editor.contains(e.target)) {
                editor.remove();
            }
        }, {once: true});
    }

    getRotationAngle(element) {
        const transform = element.style.transform;
        if (!transform) return 0;

        const match = transform.match(/rotate\(([-+]?\d+)deg\)/);
        return match ? parseInt(match[1]) : 0;
    }

    getBackgroundOpacity(element) {
        const bgColor = element.style.backgroundColor;
        if (!bgColor) return 1;

        if (bgColor.includes('rgba')) {
            const match = bgColor.match(/rgba\(.+,\s*([\d.]+)\)/);
            return match ? parseFloat(match[1]) : 1;
        }
        return 1;
    }

    setOpacity(color, opacity) {
        if (color.startsWith('rgb(')) {
            return color.replace('rgb(', 'rgba(').replace(')', `, ${opacity})`);
        }
        if (color.startsWith('#')) {
            // Convert hex to rgba
            const r = parseInt(color.substr(1, 2), 16);
            const g = parseInt(color.substr(3, 2), 16);
            const b = parseInt(color.substr(5, 2), 16);
            return `rgba(${r}, ${g}, ${b}, ${opacity})`;
        }
        return color;
    }

    saveAsHtml() {
        // Создаем копию wrapper для сохранения
        const wrapperClone = this.previewWrapper.cloneNode(true);
        const bgColor = this.previewWrapper.style.backgroundColor || 'white';
        const bgImage = this.previewWrapper.style.backgroundImage || 'none';

        // Фиксируем все блоки
        wrapperClone.querySelectorAll('.block').forEach(block => {
            // Удаляем все интерактивные элементы
            const colorPickers = block.querySelectorAll('.color-picker');
            colorPickers.forEach(picker => picker.remove());

            // Удаляем contenteditable
            const editableElements = block.querySelectorAll('[contenteditable="true"]');
            editableElements.forEach(el => el.removeAttribute('contenteditable'));

            // Фиксируем позицию и размеры
            const rect = block.getBoundingClientRect();
            const parentWidth = this.previewWrapper.offsetWidth;
            const parentHeight = this.previewWrapper.offsetHeight;

            block.style.position = 'absolute';
            block.style.left = `${(rect.left / parentWidth * 100)}%`;
            block.style.top = `${(rect.top / parentHeight * 100)}%`;
            block.style.width = `${(block.offsetWidth / parentWidth * 100)}%`;
            block.style.height = 'auto';
        });

        // Создаем полный HTML-документ
        const html = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>${this.recipeData.name}</title>
        <style>
            body { margin: 0; padding: 0; }
            .preview-wrapper {
                position: relative;
                width: 100%;
                height: 0;
                padding-bottom: 100%;
                margin: 0 auto;
                background: ${bgColor};
                background-image: ${bgImage};
                background-size: cover;
                overflow: hidden;
            }
            .block {
                position: absolute;
                box-sizing: border-box;
                padding: 15px;
                background: white;
                border: 2px solid #686F95;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .block h1, .block h2, .block h3, .block p {
                margin: 0 0 10px 0;
                color: #374967;
            }
            .block img {
                max-width: 100%;
                height: auto;
            }
        </style>
    </head>
    <body>
        <div class="preview-wrapper">
            ${wrapperClone.innerHTML}
        </div>
    </body>
    </html>
    `;

        const blob = new Blob([html], {type: 'text/html'});
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.recipeData.name.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_recipe.html`;
        a.click();

        URL.revokeObjectURL(url);
    }

// Обновите функцию saveAsPng:
    async saveAsPng() {
        try {
            // Показываем сообщение о начале процесса
            const loadingMsg = document.createElement('div');
            loadingMsg.style.position = 'fixed';
            loadingMsg.style.top = '20px';
            loadingMsg.style.left = '50%';
            loadingMsg.style.transform = 'translateX(-50%)';
            loadingMsg.style.backgroundColor = '#545B81';
            loadingMsg.style.color = 'white';
            loadingMsg.style.padding = '10px 20px';
            loadingMsg.style.borderRadius = '5px';
            loadingMsg.style.zIndex = '10000';
            loadingMsg.textContent = 'Создание PNG...';
            document.body.appendChild(loadingMsg);

            // Используем html2canvas для создания PNG
            const html2canvas = await import('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js');

            // Создаем копию wrapper для рендеринга
            const wrapperClone = this.previewWrapper.cloneNode(true);
            wrapperClone.style.transform = 'none';
            wrapperClone.style.width = '1000px';
            wrapperClone.style.height = '800px';
            wrapperClone.style.background = this.previewWrapper.style.background;
            wrapperClone.style.backgroundColor = this.previewWrapper.style.backgroundColor;
            wrapperClone.style.backgroundImage = this.previewWrapper.style.backgroundImage;

            // Фиксируем все блоки
            wrapperClone.querySelectorAll('.block').forEach(block => {
                block.style.position = 'absolute';
                const rect = block.getBoundingClientRect();
                const parentWidth = this.previewWrapper.offsetWidth;
                const parentHeight = this.previewWrapper.offsetHeight;

                block.style.left = `${(rect.left / parentWidth * 1000)}px`;
                block.style.top = `${(rect.top / parentHeight * 800)}px`;
                block.style.width = `${(block.offsetWidth / parentWidth * 1000)}px`;
            });

            // Временно добавляем клон в DOM
            wrapperClone.style.visibility = 'hidden';
            wrapperClone.style.position = 'absolute';
            wrapperClone.style.top = '0';
            wrapperClone.style.left = '0';
            document.body.appendChild(wrapperClone);

            // Конвертируем в canvas
            const canvas = await html2canvas.default(wrapperClone, {
                scale: 2,
                logging: false,
                useCORS: true,
                allowTaint: true,
                backgroundColor: null
            });

            // Удаляем клон
            document.body.removeChild(wrapperClone);

            // Создаем ссылку для скачивания
            const link = document.createElement('a');
            link.download = `${this.recipeData.name.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_recipe.png`;
            link.href = canvas.toDataURL('image/png');
            link.click();

            // Удаляем сообщение о загрузке
            loadingMsg.remove();

        } catch (error) {
            console.error('Error generating PNG:', error);
            alert('Произошла ошибка при создании PNG. Пожалуйста, попробуйте снова.');
        }
    }
}

// Initialize the form when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new RecipeForm();
});