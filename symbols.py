from typing import List, Dict, Tuple, Optional

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Dict] = {}
    
    def set_symbol(self, name: str, type: str, params: List[str] = None):
        self.symbols[name] = {
            'type': type,
            'parameters': params if params else []
        }
    
    def get_symbol(self, name: str) -> Optional[Dict]:
        return self.symbols.get(name)
    
    def print_table(self):
        name_width = max(len("Name"), max((len(name) for name in self.symbols.keys())))
        type_width = max(len("Type"), max((len(info['type']) for info in self.symbols.values())))
        params_width = max(len("Parameters"), max((len(', '.join(info['parameters'])) 
                                                for info in self.symbols.values())))
        
        horizontal_line = f"+{'-' * (name_width + 2)}+{'-' * (type_width + 2)}+{'-' * (params_width + 2)}+"
        
        print("\n\033[1m╔════════════════════════════════════╗")
        print("║            Symbol Table            ║")
        print("╚════════════════════════════════════╝\033[0m")


        print(horizontal_line)
        print(f"| {'Name':<{name_width}} | {'Type':<{type_width}} | {'Parameters':<{params_width}} |")
        print(horizontal_line)
        
        for name, info in self.symbols.items():
            params = ', '.join(info['parameters']) if info['parameters'] else ''
            print(f"| {name:<{name_width}} | {info['type']:<{type_width}} | {params:<{params_width}} |")
        
        print(horizontal_line)
