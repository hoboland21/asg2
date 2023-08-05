export interface IUser {
    first_name: string;
    last_name: string;
    username: string;
    password: string;
    email: string;
    groups: string[];
    is_staff:boolean;
    is_active: boolean;
    date_joined: Date;
    last_login: Date;
    refresh: string;
}

