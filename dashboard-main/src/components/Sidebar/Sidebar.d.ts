export interface FilterOption {
  id: string;
  label: string;
  isSelected: boolean;
}

export interface FilterSection {
  id: string;
  title: string;
  hasFilterIcon: boolean;
  options: FilterOption[];
}

export interface SidebarProps {
  className?: string;
}
