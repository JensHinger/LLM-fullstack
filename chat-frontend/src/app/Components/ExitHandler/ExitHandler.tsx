'use client'

import { useEffect } from "react"

export default function ExitHandler() {

    useEffect(() => {
        const handleUnload = () => {
            navigator.sendBeacon(`/api/exit/`)
        }

        window.addEventListener('beforeunload', handleUnload)

        return () => {
            window.removeEventListener('beforeunload', handleUnload)
        }
    }, []);

    return null;
}