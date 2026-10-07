// /** @odoo-module **/
// console.log('TEST MULTI SELECT')

import publicWidget from "@web/legacy/js/public/public_widget";

console.log('TEST MULTI SELECT')

const TagPillsWidget = publicWidget.Widget.extend({
    selector: '#tag-pills-container',
    events: { 'click .remove-tag-btn': '_onRemoveTagClick' },
    init(parent, options) {
        this._super(...arguments);
        this.selectedTags = [];
    },
    start() {
        // console.log(this.el)
        // this._updateTags();
        this.tagDropdown = this.el.querySelector('#genres');
        console.log('test :',this.tagDropdown)
        if (!this.tagDropdown) {
            console.log('NULL',this._super)
            return this._super(...arguments);
        }
        [...this.tagDropdown.options].forEach(opt => {
            if (opt.selected) this.selectedTags.push({ id: opt.value, name: opt.text.trim() });
        });

        this.tagDropdown.addEventListener("click", e => this._onTagClick(e));
        return this._super(...arguments);
    },
    _onTagClick(e) {
        console.log("bskhc")
        if (e.target.tagName !== 'OPTION') return;
        const { value: id, textContent } = e.target;
        const name = textContent.trim();
        const exists = this.selectedTags.find(t => t.id === id);
        this.selectedTags = exists
            ? this.selectedTags.filter(t => t.id !== id)
            : [...this.selectedTags, { id, name }];
        e.target.selected = !exists;
        this._updateTags();
    },
    _onRemoveTagClick(e) {
        const id = e.currentTarget.dataSet.tagId;
        this.selectedTags = this.selectedTags.filter(t => t.id !== id);
        const opt = this.tagDropdown?.querySelector('option[value="${id}"]');
        if (opt) opt.selected = false;
        this._updateTags();
    },
    _updateTags() {
        this.el.innerHTML = '';
        console.log('selected tags :',this.selectedTags)
        this.selectedTags.forEach(({ id, name }) => {
            const pill = Object.assign(document.createElement('div'), {
                className: 'tag-pill',
                style: 'background:#e6f0ff;color:#000;padding:4px 8px;border-radius:16px;font-size:14px;margin:2px;display:inline-flex;align-items:center;',
                textContent: name,
            });
            const btn = Object.assign(document.createElement('div'),{
                className: 'remove-tag-btn',
                dataSet: { tagId: id },
                style: 'background:#6c757d;color:#fff;width:18px;height:18px;display:flex;align-items:center; justify-content:center;cursor:pointer;font-size:12px;font-weight:bold;margin-left:6px;border-radius:50%;',
                textContent: '×',
            });
            pill.appendChild(btn);
            this.el.appendChild(pill);
        });
    },
});
publicWidget.registry.TagPills = TagPillsWidget;
export default TagPillsWidget;



// odoo.define('donate_book_form.m2m_widget', function (require) {
//    "use strict";
//    const publicWidget = require('web.public.widget');
//    publicWidget.registry.M2MSelectWidget = publicWidget.Widget.extend({
//        selector: '#tag-pills-container',
//        start: function () {
//            if ($(this.selector).length) {
//                $(this.selector).select2({
//                    placeholder: "Select multiple tags",
//                    width: '100%'
//                });
//            }
//        },
//    });
// });