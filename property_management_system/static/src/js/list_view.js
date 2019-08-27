odoo.define('property_management_system', function (require) {
    "use strict";
    var check = false;
    var core = require('web.core');
    var FormRenderers = require('web.FormRenderer');
    var ListView = require('web.ListView');
    var BasicModel = require('web.BasicModel');
    var _t = core._t;
    var QWeb = core.qweb;
    console.log("Hello");
    if (check == false) {
        var FormRenderer = FormRenderers.include({
            events: _.extend({}, FormRenderers.prototype.events, {
                'click .filter_search': '_onClick',
            }),
            _onClick: function (event) {
                var self = this;
                var rows = $('.temp_row').val();
                if (rows) {
                    console.log("LOG", this.state.res_id, rows);
                    var model = new BasicModel('pms.properties');
                    console.log("LOG22", model);
                    model_id = model.call('write', [[this.state.res_id], { 'rows': rows }]);
                    model.then(function (model_id) {
                        window.location.reload();
                    });
                }
                return;
                this._super();
            },
        });
        ListView.include({
            init: function () {
                var self = this;
                this._super.apply(this, arguments);

            },
            start: function () {
                var self = this;
                console.log("LOG2", this);
                this._super.apply(this, arguments);
                if (self.dataset) {
                    if (self.dataset.parent_view) {
                        if (self.dataset.parent_view.datarecord) {
                            if (self.dataset.parent_view.datarecord.rows) {
                                this._limit = self.dataset.parent_view.datarecord.rows

                            }
                        }
                    }

                }
                console.log(self.dataset.parent_view.datarecord.rows)
            },

        });
    }
    check = true;
});
