import React from 'react'
import ReactDOM from 'react-dom/client'
import { ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import App from './App'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigProvider
      locale={zhCN}
      theme={{
        token: {
          colorPrimary: '#246bfd',
          colorSuccess: '#168f67',
          colorWarning: '#d97706',
          colorError: '#d9363e',
          colorText: '#172033',
          colorTextSecondary: '#667085',
          colorBgLayout: '#f4f6f9',
          colorBorderSecondary: '#e4e8ef',
          borderRadius: 10,
          fontFamily: 'Inter, "PingFang SC", "Microsoft YaHei", sans-serif',
        },
        components: {
          Button: { controlHeight: 38, fontWeight: 600 },
          Card: { paddingLG: 18 },
          Table: { headerBg: '#f7f8fa', headerColor: '#475467' },
        },
      }}
    >
      <App />
    </ConfigProvider>
  </React.StrictMode>,
)
