/* eslint-disable @typescript-eslint/no-explicit-any */
import { Injectable } from '@angular/core';
import { ExtractinatorService, PathVariable } from 'lassy-xpath';
import { XMLParser } from 'fast-xml-parser';

@Injectable({
    providedIn: 'root',
})
export class XmlParseService {
    constructor(private extractService: ExtractinatorService) {}

    parseXml(xml: string): Promise<any> {
        return new Promise<any>((resolve, reject) => {
            try {
                const parseOptions = {
                    arrayMode: true,
                    attrNodeName: '$',
                    attributeNamePrefix: '',
                    ignoreAttributes: false,
                    parseAttributeValue: true,
                };
                const parser = new XMLParser(parseOptions);

                const data = parser.parse(xml);
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
