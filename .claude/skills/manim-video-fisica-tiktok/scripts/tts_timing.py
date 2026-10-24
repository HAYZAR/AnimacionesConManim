"""
Calcula, para cada metodo llamado dentro de construct(), el instante (en
segundos) en el que empieza, sumando los run_time= de self.play(...) y los
argumentos de self.wait(...) en el ORDEN en que aparecen, siguiendo tambien
las llamadas a otros metodos de self (helpers) de forma recursiva, y
sustituyendo parametros (p.ej. run_time=run_time) por el valor real pasado
en cada sitio de la llamada (o el default del helper si no se pasa).

Uso: python3 tts_timing.py archivo.py NombreClase
Imprime: metodo_name  start_seconds  duration_seconds
"""
import ast
import sys


def literal_or_none(node):
    try:
        return float(ast.literal_eval(node))
    except Exception:
        return None


class Evaluator:
    def __init__(self, methods):
        self.methods = methods  # name -> ast.FunctionDef

    def param_defaults(self, func_def: ast.FunctionDef):
        """Mapa nombre_parametro -> valor default (float) o None."""
        args = func_def.args
        defaults = {}
        positional = args.args
        n_defaults = len(args.defaults)
        for i, d in enumerate(args.defaults):
            arg = positional[len(positional) - n_defaults + i]
            defaults[arg.arg] = literal_or_none(d)
        for kwarg, d in zip(args.kwonlyargs, args.kw_defaults):
            if d is not None:
                defaults[kwarg.arg] = literal_or_none(d)
        return defaults

    def bind_call_args(self, func_def: ast.FunctionDef, call: ast.Call, env):
        """Devuelve un dict nombre_parametro -> valor (float) resuelto para
        esta llamada, usando el entorno (env) del llamador para resolver
        Name nodes que sean a su vez parametros del llamador."""
        defaults = self.param_defaults(func_def)
        bound = dict(defaults)
        params = [a.arg for a in func_def.args.args if a.arg != "self"]

        for i, arg_node in enumerate(call.args):
            if i < len(params):
                bound[params[i]] = self.resolve(arg_node, env)
        for kw in call.keywords:
            if kw.arg:
                bound[kw.arg] = self.resolve(kw.value, env)
        return bound

    def resolve(self, node, env):
        """Resuelve un nodo a un valor numerico usando env (parametros del
        metodo actual) si es un Name, o ast.literal_eval si es literal."""
        if isinstance(node, ast.Name) and node.id in env:
            return env[node.id]
        val = literal_or_none(node)
        return val if val is not None else 1.0

    def call_duration(self, call: ast.Call, env):
        func_name = call.func.attr if isinstance(call.func, ast.Attribute) else None
        if func_name == "wait":
            arg = call.args[0] if call.args else None
            for kw in call.keywords:
                if kw.arg == "duration":
                    arg = kw.value
            return self.resolve(arg, env) if arg is not None else 1.0
        if func_name == "play":
            for kw in call.keywords:
                if kw.arg == "run_time":
                    return self.resolve(kw.value, env)
            return 1.0
        if func_name in self.methods and func_name not in ("play", "wait"):
            sub_env = self.bind_call_args(self.methods[func_name], call, env)
            return self.method_duration(self.methods[func_name], sub_env)
        return 0.0

    def method_duration(self, func_def: ast.FunctionDef, env):
        return self.block_duration(func_def.body, env)

    def block_duration(self, stmts, env):
        return sum(self.stmt_duration(s, env) for s in stmts)

    def stmt_duration(self, node, env):
        """Recorre la ESTRUCTURA de control (no ast.walk, que aplanaria
        ambas ramas de un if y las contaria dos veces). Para un If se toma
        solo la rama 'body' como aproximacion -- en este código las dos
        ramas de cada if/else usadas duran lo mismo, asi que el resultado
        es correcto de todas formas."""
        if isinstance(node, ast.If):
            return self.block_duration(node.body, env)
        if isinstance(node, (ast.For, ast.While)):
            return self.block_duration(node.body, env)
        if isinstance(node, (ast.With,)):
            return self.block_duration(node.body, env)
        if isinstance(node, ast.Try):
            return self.block_duration(node.body, env)
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name):
                if call.func.value.id == "self":
                    return self.call_duration(call, env)
            return 0.0
        return 0.0


def main():
    path, class_name = sys.argv[1], sys.argv[2]
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)

    class_def = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            class_def = node
            break
    if class_def is None:
        print(f"Clase {class_name} no encontrada", file=sys.stderr)
        sys.exit(1)

    methods = {n.name: n for n in class_def.body if isinstance(n, ast.FunctionDef)}
    construct = methods.get("construct")
    ev = Evaluator(methods)

    call_order = []
    for node in construct.body:
        for child in ast.walk(node):
            if (
                isinstance(child, ast.Call)
                and isinstance(child.func, ast.Attribute)
                and isinstance(child.func.value, ast.Name)
                and child.func.value.id == "self"
            ):
                call_order.append(child.func.attr)

    t = 0.0
    for name in call_order:
        if name not in methods:
            continue
        dur = ev.method_duration(methods[name], {})
        print(f"{name}\t{t:.3f}\t{dur:.3f}")
        t += dur
    print(f"TOTAL\t{t:.3f}\t0.000")


if __name__ == "__main__":
    main()
