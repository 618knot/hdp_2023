import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const errorNotification = (message: string) => {
    return toast.error(message)
};

export const successNotification = (message: string) => {
    return toast.success(message)
};