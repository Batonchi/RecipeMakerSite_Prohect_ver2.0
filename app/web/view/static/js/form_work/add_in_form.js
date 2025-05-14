class Patterns {
    'step'  = {
        'value': '<div class="steps__elem">\n' +
            '                            <div class="block--flex_row">\n' +
            '                                <div class="block--flex_column">\n' +
            '                                    <div class="grid_input_custom_label var_grid_1">\n' +
            '                                        <div class="label_back border_bottom_right_top_left">имя</div>\n' +
            '                                        <input type="text" class="border_bottom style_font limit_width_input" required>\n' +
            '                                        <div class="border_bottom label_back">номер</div>\n' +
            '                                        <input type="text" class="style_font border_top_right_bottom_left limit_width_input" required>\n' +
            '                                    </div>\n' +
            '                                    <div class="grid_input_custom_label var_grid_2">\n' +
            '                                        <div class="label_back border_right">описание</div>\n' +
            '                                        <textarea type="text" id="description" class="style_font border_left" required style="resize: none; border: none"></textarea>\n' +
            '                                        <div class="label_back border_top_right_bottom_left">пояснение</div>\n' +
            '                                        <textarea type="text" id="additional_info" class="style_font border_bottom_right_top_left" required style="resize: none; border: none"></textarea>\n' +
            '                                    </div>\n' +
            '                                    <div class="step--add_graphic border_top border_bottom">\n' +
            '                                        <div id="container_graph" class="border_bottom border_top container">\n' +
            '                                            выберите графическую состовляющею этапа\n' +
            '                                        </div>\n' +
            '                                        <button class="border_bottom button--add_images">+</button>\n' +
            '                                    </div>\n' +
            '                                    <div class="step--add_links links--add  border_bottom border_top">\n' +
            '                                        <div class="container border_bottom border_top" id="step_links">\n' +
            '                                            <input type="text" placeholder="куда ведет" class="where border_bottom border_top" required>\n' +
            '                                            <input type="text" placeholder="ссылка" class="link_str border_bottom border_top" required>\n' +
            '                                        </div>\n' +
            '                                        <div class="between_link_and_add  border_bottom border_top">нажмите +, чтобы добавить ссылку</div>\n' +
            '                                        <button class="add-button border_bottom">+</button>\n' +
            '                                    </div>\n' +
            '                                </div>\n' +
            '                                <button class="step__elem--del">x</button>\n' +
            '                            </div>\n' +
            '                        </div>'
    }
    'link' = {
        'value': '<input type="text" placeholder="куда ведет" class="where border_bottom border_top" required>\n' +
            '                                            <input type="text" placeholder="ссылка" class="link_str border_bottom border_top" required>'
    }
    'ingredient' = {
        'value': '<div class="ingredient block--flex_row">\n' +
            '                                <label class="id_ing">1</label>\n' +
            '                                <input type="text" id="name_ing" class="style_font" placeholder="наименование">\n' +
            '                                <input type="text" id="for_need" class="style_font" placeholder="для чего">\n' +
            '                                <input type="text" id="count" class="style_font" placeholder="кол-во">\n' +
            '                                <label class="label__button--delete_ing">x</label>\n' +
            '                            </div>'
    }
}


 export class AddInForm {
    constructor(container = document.body, pattern = null) {
        this._pattern = pattern ? pattern : null
        this._container = container
    }

    static addingImages() {
        return null
    }

    addInfoInContainer() {
        this._container.appendChild(this._pattern)
    }



}