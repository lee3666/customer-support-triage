'use client'
import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import axios from 'axios'

interface User {
  id: string
  email: string
  full_name: string
  role: string
  is_active: boolean
  created_at: string
}

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, fullName: string, password: string, role: string) => Promise<void>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUserData()
  }, [])

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        setLoading(false)
        return
      }

      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      const response = await axios.get('http://localhost:8001/auth/me')
      setUser(response.data)
    } catch (error: any) {
      console.error('Failed to fetch user data:', error)
      
      // Clear invalid token on 401
      if (error.response?.status === 401) {
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
      }
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post('http://localhost:8001/auth/login', {
        email,
        password
      })
      
      const { access_token, user: userData } = response.data
      localStorage.setItem('token', access_token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      setUser(userData)
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed')
    }
  }

  const register = async (email: string, fullName: string, password: string, role: string = 'customer') => {
    try {
      const response = await axios.post('http://localhost:8001/auth/register', {
        email,
        full_name: fullName,
        password,
        role
      })
      
      const { access_token, user: userData } = response.data
      localStorage.setItem('token', access_token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      setUser(userData)
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed')
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
  }

  const value = {
    user,
    login,
    register,
    logout,
    loading
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
