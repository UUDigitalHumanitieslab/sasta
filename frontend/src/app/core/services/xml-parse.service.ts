import { Injectable } from '@angular/core';
import { ExtractinatorService, PathVariable } from 'lassy-xpath';
import * as parser from 'fast-xml-parser';

@Injectable({
    providedIn: 'root',
})
export class XmlParseService {
    constructor(private extractService: ExtractinatorService) {}

    parseXml(xml: string): Promise<any> {
        return new Promise<any>((resolve, reject) => {
            try {
                const data = parser.parse(xml, {
                    arrayMode: true,
                    attrNodeName: '$',
                    attributeNamePrefix: '',
                    ignoreAttributes: false,
                    parseAttributeValue: true,
                });
                return resolve(data);
            } catch (exception) {
                return reject(exception);
            }
        });
    }

    extractVariables(xpath: string): any {
        let variables: PathVariable[];
        try {
            variables = this.extractService.extract(xpath);
        } catch (e) {
            variables = [];
            console.warn('Error extracting variables from path', e, xpath);
        }

        return {
            variables,
            lookup: variables.reduce<{ [name: string]: PathVariable }>(
                (vs, v) => {
                    vs[v.name] = v;
                    return vs;
                },
                {}
            ),
        };
    }
}
