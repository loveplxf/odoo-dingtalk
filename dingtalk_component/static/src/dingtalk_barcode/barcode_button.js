/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { Tooltip } from "@web/core/tooltip/tooltip";
import { usePopover } from "@web/core/popover/popover_hook";
import { Component, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { useService } from "@web/core/utils/hooks";
import { ConfirmationDialog, AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class BarcodeButton extends Component {
    static template = "web.BarcodeButton";
    static props = {
        id: { type: String, optional: true },
        name: { type: String },
        readonly: { type: Boolean, optional: true },
        record: { type: Object },
        className: { type: String, optional: true },
        copyText: { type: String, optional: true },
        disabled: { type: Boolean, optional: true },
        successText: { type: String, optional: true },
        content: { type: [String, Object], optional: true },
    };

    setup() {
        this.button = useRef("button");
        this.dialog = useService("dialog");
        useInputField({ getValue: () => this.props.record.data[this.props.name] || "" });
    }

    async onClick() {
        var self = this;
        if(dd.version) {
            dd.biz.util.scan({
                type: 'all',
                onSuccess: function(data) {
                    var barcode = data.text;
                    if (barcode){
                        self.props.record.update({ [self.props.name]: barcode });
                        dd.device.notification.vibrate({'duration': 100});
                    } else {
                        dd.device.notification.toast({'text': '扫码故障，请再次扫描'});
                    }
                },
                onFail: function(err) {
                    dd.device.notification.toast({'text': '扫码故障，请再次扫描'});
                }
            });
        }else{
            this.dialog.add(AlertDialog, {
                            title: "提示",
                            body: "该功能仅支持钉钉手机客户端使用"
                        });
        }
    }
}

function extractProps({ attrs }) {
    return {
        string: attrs.string,
        disabledExpr: attrs.disabled,
    };
}

export const barcodeButton = {
    component: BarcodeButton,
    displayName: _t("Barcode"),
    supportedTypes: ["char"],
    extractProps,
};

registry.category("fields").add("dingtalk_barcode", barcodeButton);