import { useTheme } from './ThemeProvider';

export default function Header() {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <header className="border-b border-border bg-card">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <i className="fas fa-robot text-primary-foreground text-lg"></i>
            </div>
            <div>
              <h1 className="text-xl font-semibold text-card-foreground">CV Chatbot</h1>
              <p className="text-sm text-muted-foreground">Interactive Resume Assistant</p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <button 
              onClick={toggleTheme}
              data-testid="button-theme-toggle"
              className="relative inline-flex h-6 w-11 items-center rounded-full bg-muted transition-colors hover:bg-accent focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            >
              <span className="sr-only">Toggle theme</span>
              <span 
                className={`inline-block h-4 w-4 transform rounded-full bg-card transition duration-200 ease-in-out ${
                  theme === 'dark' ? 'translate-x-6' : 'translate-x-1'
                }`}
              >
                <i className={`${
                  theme === 'dark' 
                    ? 'fas fa-moon text-slate-300' 
                    : 'fas fa-sun text-yellow-500'
                } text-xs flex items-center justify-center h-full`}></i>
              </span>
            </button>

            <div className="text-sm text-muted-foreground">
              <span>Mohammed Alakhras</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}