// import {createContext, useEffect, useState} from "react";
// import {AuthContextType, AuthProviderProps, User} from "@/types/AuthTypes.tsx";
// import {useNavigate} from "react-router-dom";
// import {apiCall} from "@/utils/ApiCall.tsx";
//
// const AuthContext = createContext<AuthContextType>({} as AuthContextType);
//
// export const AuthProvider = ({ children }: AuthProviderProps) => {
//     const navigate = useNavigate();
//     const [user, setUser] = useState<User | null>(null);
//     const [isReady, setIsReady] = useState(false);
//
//     useEffect(() => {
//         const user = localStorage.getItem("user");
//         if (user) {
//             setUser(JSON.parse(user));
//         }
//         setIsReady(true);
//         }, []);
//
//     const register = async (
//         username: string,
//         displayName: string,
//         password: string
//     ) => {
//         await apiCall(
//             'authors/signup',
//             "POST",
//             {
//               username: username,
//               password: password,
//               displayName: displayName,
//               profileImage: `https://robohash.org/${displayName}.png`
//             }
//             ).then((res) => {
//                 if (res) {
//                     localStorage.setItem("")
//                 }
//         })
//     }
//
// }