import { trigger, style, transition, animate, state } from '@angular/animations';

export type ShowState = 'hide' | 'show';

export const animations = [
    trigger('slideInOut', [
        state(
            'show',
            style({
                height: '*',
            })
        ),
        state(
            'hide',
            style({
                height: '0px',
                // eslint-disable-next-line @typescript-eslint/naming-convention
                'padding-top': '0px',
                // eslint-disable-next-line @typescript-eslint/naming-convention
                'padding-bottom': '0px',
                overflow: 'hidden',
            })
        ),
        transition('show => hide', [animate('0.2s')]),
        transition('hide => show', [animate('0.2s')]),
    ]),
];
