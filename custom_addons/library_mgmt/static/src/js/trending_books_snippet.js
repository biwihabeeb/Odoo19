/** @odoo-module **/
import { renderToElement } from "@web/core/utils/render";
import PublicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

console.log('SNIPPET TEST...')
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.books.length; i = i + size) {
        result.push(array.books.slice(i, i+size));
    }
    return result;
}
export function _generateRandomId() {
    let length = 10
    const characters = 'abcdefghijklmnopqrstuvwxyz';
    let result = '';
    const charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}
let TopTrendingBooks = PublicWidget.Widget.extend({
    selector: '.trending_books_snippet',
    async willStart() {

        const data = await rpc('/get_trending_books', {});
        // console.log(data)
        const books = data;
        Object.assign(this, {
            books
        });
    },
    start: function () {
        // console.log('Start...');
        const refEl = this.$el.find('#book_carousel');
        const books = this;
        const divEl = document.getElementById("trending_book_carousel")
        const randId = _generateRandomId();
        divEl.id = randId
        const sliderPrevEl = document.getElementsByClassName("carousel-control-prev");
        const sliderNextEl = document.getElementsByClassName("carousel-control-next");
        sliderPrevEl[0].hash = "#"+randId;
        sliderNextEl[0].hash = "#"+randId;
        const chunkSize = 3;
        const maxWidth = 100 / chunkSize
        // console.log('SLIDER: ',sliderEl[0].hash)
        const chunkData = _chunk(books.books, chunkSize);

        chunkData[0].is_active = true;
        // console.log('CHUNK DATA',chunkData);
        // console.log('ref el :',refEl.id)
        refEl.html(renderToElement('library_mgmt.trending_books_snippet_carousel_template', {chunkData, maxWidth}));

    }
});
PublicWidget.registry.trending_books_carousel_snippet = TopTrendingBooks;
return TopTrendingBooks;




