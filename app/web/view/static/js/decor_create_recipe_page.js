export class DecorativeWaveElement {
    constructor(width = 100, height = 100, sep = 0,
                image_url_num = 1, where = document.body) {
        this._width = width;
        this._height = height;
        this._sep = sep;
        this._where = where
        this._start_image_url = image_url_num
        this._paste_params = {
            1: 'afterbegin',
            2: 'afterend',
            3: 'beforeend',
            4: 'beforebegin'
        }
        this._urls_images = {
            1: '/static/images/create_recipe/wave.svg',
            2: '/static/images/create_recipe/wave_180.svg',
            3: '/static/images/create_recipe/vert_wave.svg',
            4: '/static/images/create_recipe/vert_wave_180.svg',
        }
        this._image_url = this._urls_images[image_url_num]
    }

    get width() {
        return this._width
    }

    get height() {
        return this._height
    }

    show(repeat = 1, insert_where = 1, move_right = 0, dop_elem_height = 0, paste_where = this._where) {
        console.log('Using image URL:', this._image_url); // Для отладки
        let container = document.createElement('div')
            container.className = 'container'
            container.style.cssText = `
                display: flex;
                flex-direction: column;
                height: max-content;
                width: max-content;
                gap: ${this._sep};
            `
        for (let i = 0; i <= repeat; i++) {
            if (i % 2 === 0 && this._start_image_url % 2 !== 0) {
                this._image_url = this._urls_images[1]
        } else if (i % 2 !== 0 && this._start_image_url % 2 !== 0){
                this._image_url = this._urls_images[3]
        } else if (i % 2 === 0 && this._start_image_url % 2 === 0) {
                this._image_url = this._urls_images[2]
            } else  {
                this._image_url = this._urls_images[4]
            }
            let elem = document.createElement('div');
            elem.className = 'container__block--style';
            let content = `
                display: block;
                width: ${this._width}px;
                background-image: url('${this._image_url}');
                background-repeat: no-repeat;
                background-size: cover;
            `;
            if (i !== repeat) {
                content += `height: ${this._height}px;`
            }
            if (move_right === 0) {
                content += `transform: translate(-5px, ${-120 -i * 20}px);`
            } else {
                content += `transform: translate(5px, ${-120 -i * 20}px);`
            }
            elem.style.cssText = content
            container.appendChild(elem)
        }
        paste_where.insertAdjacentElement(this._paste_params[insert_where], container)
    }
}