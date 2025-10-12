export function debounce<T>(func: (arg: T) => void, delay: number) {
  let debounceTimer: ReturnType<typeof setTimeout>;
  return function debouncedFunction(arg: T) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => func(arg), delay);
  };
}
