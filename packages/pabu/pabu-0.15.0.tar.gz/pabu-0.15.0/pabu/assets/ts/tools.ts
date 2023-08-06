import { LocalStorageSchema, AppData } from "./types";

const durationDesc = [
    {divider: 3600, unit: 'hour'},
    {divider: 60, unit: 'minute'},
    {divider: 1, unit: 'second'},
];

export function formatDuration(value: number): string {

    let isNeg = value < 0;

    if (isNeg)
        value = -value;

    let resValue = 0;
    let resUnit = 'second';

    for (let d of durationDesc) {
        let dv = value / d.divider;
        if (dv >= 1) {
            resValue = dv;
            resUnit = d.unit;
            break;
        }
    }

    return `${(isNeg ? -resValue : resValue).toFixed(1)} ${resUnit}` + (resValue > 1 ? 's' : '');
}

export function formatStopwatchDuration(value: number): string {
    const hours = Math.floor(value/3600);
    const minutes = Math.floor(value % 3600 / 60);
    const seconds = Math.floor(value % 60);

    const num = (v: number) => v.toString().padStart(2, '0')

    return `${num(hours)}:${num(minutes)}:${num(seconds)}`
}

const localStorageHandler = {
    get: (target: LocalStorageSchema, name: string) => {
        const res = window.localStorage.getItem(name);
        return res == undefined ? target[name] : JSON.parse(res);
    },
    set: (target: LocalStorageSchema, name: string, value: any, receiver: any) => {
        window.localStorage.setItem(name, JSON.stringify(value));
        return true;
    },
}

export const pabuLocalStorage = new Proxy<LocalStorageSchema>(new LocalStorageSchema(), localStorageHandler);

export function capitalizeFirstLetter(string: string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

export type StringObject = {[s: string]: any};

export function convertKeysToSnakeCase(data: StringObject): StringObject {
    let res = {}
    for (const key in data) {
        res[key.split(/(?=[A-Z])/).map(s => s.toLowerCase()).join('_')] = data[key];
    }
    return res
}

export const isObject = function(a) {
    return (!!a) && (a.constructor === Object);
};

export function convertKeysToCamelCase<T>(data: T): T {
    let res = {} as T
    for (const key in data) {
        let newKey = key.split('_').map(s => capitalizeFirstLetter(s)).join('');
        let value = data[key];
        res[newKey.charAt(0).toLowerCase() + newKey.slice(1)] = isObject(value) ? convertKeysToCamelCase(value) : value;
    }
    return res
}

export function removeKeys<T extends object>(data: T, ...keys: Array<string>): T {
    return Object.keys(data).filter(k => keys.indexOf(k) == -1).reduce((map, key) => (map[key] = data[key], map), {}) as T;
}

export function filterDataProps(props: StringObject): StringObject {
    let res = {};
    for (const key in props) {
        if (key.startsWith('data-'))
            res[key] = props[key];
    }
    return res;
}

export const appData = window['appData'] as AppData;
