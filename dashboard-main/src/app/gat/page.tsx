'use client';

import { useState } from 'react';
import { Table, When } from 'vizonomy';
import type { TableColumn } from 'vizonomy';

// Sample data types for table examples
interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  status: 'active' | 'inactive';
  createdAt: Date;
}

interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  stock: number;
  available: boolean;
}

interface Transaction {
  id: string;
  date: string;
  description: string;
  category: string;
  subcategory: string;
  merchant: string;
  amount: number;
  balance: number;
  status: 'pending' | 'completed' | 'failed';
  reference: string;
  notes?: string;
}

interface Employee {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  department: string;
  position: string;
  salary: number;
  hireDate: Date;
  status: 'active' | 'inactive' | 'on-leave';
  manager?: string;
  skills: string[];
  performance: number;
}

export default function GAT() {
  // Table state management
  const [selectedRowKeys, setSelectedRowKeys] = useState<string[]>([]);
  const [selectedRows, setSelectedRows] = useState<Product[]>([]);
  const [employeeSelectedRowKeys, setEmployeeSelectedRowKeys] = useState<
    string[]
  >([]);
  const [employeeSelectedRows, setEmployeeSelectedRows] = useState<Employee[]>(
    []
  );

  // Sample data for table examples
  const userData: User[] = [
    {
      id: '1',
      name: 'John Doe',
      email: 'john@worldbank.org',
      role: 'Senior Analyst',
      status: 'active',
      createdAt: new Date('2023-01-15'),
    },
    {
      id: '2',
      name: 'Jane Smith',
      email: 'jane@worldbank.org',
      role: 'Project Manager',
      status: 'active',
      createdAt: new Date('2023-02-20'),
    },
    {
      id: '3',
      name: 'Bob Johnson',
      email: 'bob@worldbank.org',
      role: 'Data Scientist',
      status: 'inactive',
      createdAt: new Date('2023-03-10'),
    },
    {
      id: '4',
      name: 'Alice Brown',
      email: 'alice@worldbank.org',
      role: 'Research Lead',
      status: 'active',
      createdAt: new Date('2023-04-05'),
    },
    {
      id: '5',
      name: 'Charlie Wilson',
      email: 'charlie@worldbank.org',
      role: 'Policy Advisor',
      status: 'active',
      createdAt: new Date('2023-05-12'),
    },
  ];

  const productData: Product[] = [
    {
      id: '1',
      name: 'Development Report 2024',
      category: 'Publications',
      price: 45.99,
      stock: 15,
      available: true,
    },
    {
      id: '2',
      name: 'Economic Analysis Tool',
      category: 'Software',
      price: 299.99,
      stock: 8,
      available: true,
    },
    {
      id: '3',
      name: 'Policy Framework Guide',
      category: 'Publications',
      price: 29.99,
      stock: 25,
      available: true,
    },
    {
      id: '4',
      name: 'Data Visualization Suite',
      category: 'Software',
      price: 199.99,
      stock: 0,
      available: false,
    },
    {
      id: '5',
      name: 'Regional Assessment Kit',
      category: 'Tools',
      price: 79.99,
      stock: 12,
      available: true,
    },
    {
      id: '6',
      name: 'Impact Measurement Tool',
      category: 'Software',
      price: 149.99,
      stock: 5,
      available: true,
    },
  ];

  const transactionData: Transaction[] = [
    {
      id: '1',
      date: '2024-01-15',
      description: 'Project Funding - Education Initiative',
      category: 'Funding',
      subcategory: 'Education',
      merchant: 'Ministry of Education',
      amount: 2500000.0,
      balance: 15750000.5,
      status: 'completed',
      reference: 'WB-EDU-001-2024',
      notes: 'Primary education infrastructure',
    },
    {
      id: '2',
      date: '2024-01-14',
      description: 'Healthcare Program Disbursement',
      category: 'Funding',
      subcategory: 'Healthcare',
      merchant: 'Health Ministry',
      amount: 1800000.0,
      balance: 13250000.5,
      status: 'completed',
      reference: 'WB-HLT-002-2024',
    },
    {
      id: '3',
      date: '2024-01-13',
      description: 'Administrative Costs',
      category: 'Operations',
      subcategory: 'Administration',
      merchant: 'WB Operations',
      amount: -45000.0,
      balance: 11450000.5,
      status: 'completed',
      reference: 'WB-ADM-003-2024',
    },
    {
      id: '4',
      date: '2024-01-12',
      description: 'Infrastructure Development',
      category: 'Development',
      subcategory: 'Infrastructure',
      merchant: 'Construction Corp',
      amount: 3200000.0,
      balance: 11495000.5,
      status: 'pending',
      reference: 'WB-INF-004-2024',
    },
  ];

  const employeeData: Employee[] = [
    {
      id: '1',
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@worldbank.org',
      department: 'Development Economics',
      position: 'Senior Economist',
      salary: 125000,
      hireDate: new Date('2020-03-15'),
      status: 'active',
      manager: 'Jane Smith',
      skills: ['Economic Analysis', 'Policy Research', 'Data Analysis'],
      performance: 4.5,
    },
    {
      id: '2',
      firstName: 'Jane',
      lastName: 'Smith',
      email: 'jane.smith@worldbank.org',
      department: 'Development Economics',
      position: 'Department Director',
      salary: 180000,
      hireDate: new Date('2018-01-10'),
      status: 'active',
      skills: ['Leadership', 'Strategic Planning', 'International Development'],
      performance: 4.8,
    },
    {
      id: '3',
      firstName: 'Mike',
      lastName: 'Johnson',
      email: 'mike.johnson@worldbank.org',
      department: 'Communications',
      position: 'Communications Specialist',
      salary: 85000,
      hireDate: new Date('2021-06-20'),
      status: 'active',
      manager: 'Sarah Wilson',
      skills: ['Public Relations', 'Content Strategy', 'Digital Media'],
      performance: 4.2,
    },
    {
      id: '4',
      firstName: 'Sarah',
      lastName: 'Wilson',
      email: 'sarah.wilson@worldbank.org',
      department: 'Communications',
      position: 'Communications Director',
      salary: 145000,
      hireDate: new Date('2019-11-05'),
      status: 'on-leave',
      skills: [
        'Strategic Communications',
        'Team Management',
        'Media Relations',
      ],
      performance: 4.6,
    },
    {
      id: '5',
      firstName: 'Robert',
      lastName: 'Brown',
      email: 'robert.brown@worldbank.org',
      department: 'Operations',
      position: 'Operations Analyst',
      salary: 95000,
      hireDate: new Date('2022-02-14'),
      status: 'active',
      manager: 'Lisa Davis',
      skills: ['Project Management', 'Risk Analysis', 'Operations Research'],
      performance: 3.9,
    },
    {
      id: '6',
      firstName: 'Lisa',
      lastName: 'Davis',
      email: 'lisa.davis@worldbank.org',
      department: 'Operations',
      position: 'Operations Manager',
      salary: 135000,
      hireDate: new Date('2019-09-12'),
      status: 'active',
      skills: [
        'Operations Management',
        'Process Optimization',
        'Team Leadership',
      ],
      performance: 4.4,
    },
  ];

  // Column definitions
  const userColumns: TableColumn<User>[] = [
    {
      id: 'name',
      key: 'name',
      label: 'Name',
      sortable: true,
      width: 200,
    },
    {
      id: 'email',
      key: 'email',
      label: 'Email',
      sortable: true,
      width: 250,
    },
    {
      id: 'role',
      key: 'role',
      label: 'Role',
      sortable: true,
      width: 180,
    },
    {
      id: 'status',
      key: 'status',
      label: 'Status',
      width: 100,
      render: (value: User['status']) => {
        const v = value as string;
        return (
          <span
            className={`px-2 py-1 rounded-full text-xs font-medium ${
              v === 'active'
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }`}
          >
            {v}
          </span>
        );
      },
    },
    {
      id: 'createdAt',
      key: 'createdAt',
      label: 'Joined',
      sortable: true,
      width: 120,
      render: (value: Date) => value.toLocaleDateString(),
    },
  ];

  const productColumns: TableColumn<Product>[] = [
    {
      id: 'name',
      key: 'name',
      label: 'Product Name',
      sortable: true,
      width: 250,
    },
    {
      id: 'category',
      key: 'category',
      label: 'Category',
      sortable: true,
      width: 150,
    },
    {
      id: 'price',
      key: 'price',
      label: 'Price',
      sortable: true,
      width: 120,
      align: 'right',
      render: (value: number) => `$${value.toFixed(2)}`,
    },
    {
      id: 'stock',
      key: 'stock',
      label: 'Stock',
      sortable: true,
      width: 100,
      align: 'center',
      render: (value: number) => {
        const v = value as number;
        return (
          <span
            className={`px-2 py-1 rounded text-xs font-medium ${
              v === 0
                ? 'bg-red-100 text-red-800'
                : v < 10
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-green-100 text-green-800'
            }`}
          >
            {v}
          </span>
        );
      },
    },
    {
      id: 'available',
      key: 'available',
      label: 'Available',
      width: 100,
      align: 'center',
      render: (value: boolean) => (
        <span
          className={`w-3 h-3 rounded-full inline-block ${
            (value as boolean) ? 'bg-green-500' : 'bg-red-500'
          }`}
        />
      ),
    },
  ];

  const transactionColumns: TableColumn<Transaction>[] = [
    {
      id: 'date',
      key: 'date',
      label: 'Date',
      sortable: true,
      width: 120,
      fixed: 'left',
    },
    {
      id: 'description',
      key: 'description',
      label: 'Description',
      width: 300,
      fixed: 'left',
    },
    {
      id: 'category',
      key: 'category',
      label: 'Category',
      sortable: true,
      width: 150,
    },
    {
      id: 'subcategory',
      key: 'subcategory',
      label: 'Subcategory',
      sortable: true,
      width: 150,
    },
    {
      id: 'merchant',
      key: 'merchant',
      label: 'Merchant/Entity',
      sortable: true,
      width: 200,
    },
    {
      id: 'reference',
      key: 'reference',
      label: 'Reference',
      width: 160,
    },
    {
      id: 'notes',
      key: 'notes',
      label: 'Notes',
      width: 200,
      render: (value: string | undefined) => value || '-',
    },
    {
      id: 'status',
      key: 'status',
      label: 'Status',
      width: 120,
      render: (value: Transaction['status']) => {
        const v = value as string;
        return (
          <span
            className={`px-2 py-1 rounded-full text-xs font-medium ${
              v === 'completed'
                ? 'bg-green-100 text-green-800'
                : v === 'pending'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
            }`}
          >
            {v}
          </span>
        );
      },
    },
    {
      id: 'amount',
      key: 'amount',
      label: 'Amount',
      sortable: true,
      width: 150,
      align: 'right',
      fixed: 'right',
      render: (value: number) => {
        const v = value as number;
        return (
          <span
            className={
              v >= 0 ? 'text-green-600 font-medium' : 'text-red-600 font-medium'
            }
          >
            {v >= 0 ? '+' : ''}${Math.abs(v).toLocaleString()}
          </span>
        );
      },
    },
    {
      id: 'balance',
      key: 'balance',
      label: 'Balance',
      sortable: true,
      width: 150,
      align: 'right',
      fixed: 'right',
      render: (value: number) => {
        const v = value as number;
        return (
          <span
            className={
              v >= 0
                ? 'text-green-600 font-semibold'
                : 'text-red-600 font-semibold'
            }
          >
            ${v.toLocaleString()}
          </span>
        );
      },
    },
  ];

  const employeeColumns: TableColumn<Employee>[] = [
    {
      id: 'name',
      key: 'firstName',
      label: 'Name',
      sortable: true,
      width: 200,
      fixed: 'left',
      render: (_value: unknown, row: Employee) => (
        <div className="flex flex-col">
          <span className="font-medium">
            {row.firstName} {row.lastName}
          </span>
          <span className="text-xs text-gray-500">{row.email}</span>
        </div>
      ),
    },
    {
      id: 'department',
      key: 'department',
      label: 'Department',
      sortable: true,
      width: 180,
    },
    {
      id: 'position',
      key: 'position',
      label: 'Position',
      sortable: true,
      width: 200,
    },
    {
      id: 'manager',
      key: 'manager',
      label: 'Manager',
      width: 150,
      render: (value: string | undefined) => value || 'N/A',
    },
    {
      id: 'salary',
      key: 'salary',
      label: 'Salary',
      sortable: true,
      width: 130,
      align: 'right',
      render: (value: number) => `$${value.toLocaleString()}`,
    },
    {
      id: 'hireDate',
      key: 'hireDate',
      label: 'Hire Date',
      sortable: true,
      width: 120,
      render: (value: Date) => value.toLocaleDateString(),
    },
    {
      id: 'skills',
      key: 'skills',
      label: 'Skills',
      width: 250,
      render: (value: string[]) => {
        const v = value as string[];
        return (
          <div className="flex flex-wrap gap-1">
            {v.slice(0, 2).map((skill) => (
              <span
                key={skill}
                className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
              >
                {skill}
              </span>
            ))}
            {v.length > 2 && (
              <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                +{v.length - 2}
              </span>
            )}
          </div>
        );
      },
    },
    {
      id: 'performance',
      key: 'performance',
      label: 'Performance',
      sortable: true,
      width: 130,
      align: 'center',
      render: (value: number) => {
        const v = value as number;
        return (
          <div className="flex items-center justify-center gap-1">
            <span className="text-sm font-medium">{v.toFixed(1)}</span>
            <div className="flex">
              {[1, 2, 3, 4, 5].map((star) => (
                <svg
                  key={star}
                  className={`w-3 h-3 ${star <= v ? 'text-yellow-400' : 'text-gray-300'}`}
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              ))}
            </div>
          </div>
        );
      },
    },
    {
      id: 'status',
      key: 'status',
      label: 'Status',
      width: 110,
      fixed: 'right',
      render: (value: Employee['status']) => {
        const v = value as string;
        return (
          <span
            className={`px-2 py-1 rounded-full text-xs font-medium ${
              v === 'active'
                ? 'bg-green-100 text-green-800'
                : v === 'on-leave'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
            }`}
          >
            {v.replace('-', ' ')}
          </span>
        );
      },
    },
  ];

  // Event handlers
  const handleProductSelectionChange = (keys: string[], rows: Product[]) => {
    setSelectedRowKeys(keys);
    setSelectedRows(rows);
  };

  const handleEmployeeSelectionChange = (keys: string[], rows: Employee[]) => {
    setEmployeeSelectedRowKeys(keys);
    setEmployeeSelectedRows(rows);
  };

  const isProductRowDisabled = (row: Product) => !row.available;
  const isEmployeeRowDisabled = (row: Employee) => row.status !== 'active';

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          GAT Dashboard - Component Showcase
        </h1>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Global Assessment Tool
          </h2>
          <p className="text-gray-600 mb-4">
            This is the GAT (Global Assessment Tool) section of the World Bank
            dashboard.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-medium text-gray-900 mb-2">
                Assessment Metrics
              </h3>
              <p className="text-sm text-gray-600">
                Track and analyze global development metrics and indicators.
              </p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-medium text-gray-900 mb-2">
                Data Visualization
              </h3>
              <p className="text-sm text-gray-600">
                Interactive charts and graphs for comprehensive data analysis.
              </p>
            </div>
          </div>
        </div>

        {/* Table Examples */}
        <div className="space-y-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900">
            Headless Table Component Demo
          </h2>
          <p className="text-gray-600 mb-6">
            Comprehensive demonstration of our headless Table component with all
            features: pagination, sorting, selection, fixed columns,
            horizontal/vertical scrolling, and custom rendering.
          </p>

          {/* Basic Table Example */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              1. Basic Table with Pagination & Sorting
            </h3>
            <p className="text-gray-600 mb-4">
              Simple table demonstrating basic features: sortable columns,
              pagination, and custom cell rendering.
            </p>

            <Table
              data={userData}
              columns={userColumns}
              bordered
              hoverable
              striped
              pagination={{
                page: 1,
                pageSize: 3,
                total: userData.length,
                showSizeChanger: true,
                showTotal: true,
                pageSizeOptions: [3, 5, 10],
              }}
            />
          </div>

          {/* Selectable Table Example */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              2. Selectable Table with Business Logic
            </h3>
            <p className="text-gray-600 mb-4">
              Table with row selection, disabled rows, and real-time selection
              statistics.
            </p>

            <div className="mb-4 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold mb-2">Selection Info:</h4>
              <p className="text-sm text-gray-700">
                Selected {selectedRowKeys.length} of{' '}
                {productData.filter((row) => !isProductRowDisabled(row)).length}{' '}
                available products
              </p>
              <When condition={Boolean(selectedRows.length)}>
                <div className="mt-2">
                  <p className="text-sm font-medium">Selected Products:</p>
                  <ul className="text-sm text-gray-600 mt-1">
                    {selectedRows.map((row: Product) => (
                      <li key={row.id}>
                        • {row.name} - ${row.price}
                      </li>
                    ))}
                  </ul>
                </div>
              </When>
            </div>

            <Table
              data={productData}
              columns={productColumns}
              selection={{
                type: 'multiple',
                selectedRowKeys,
                onSelectionChange: handleProductSelectionChange,
                getRowKey: (row: Product) => row.id,
                disabled: isProductRowDisabled,
              }}
              pagination={{
                page: 1,
                pageSize: 4,
                total: productData.length,
                showSizeChanger: true,
                showTotal: true,
              }}
              bordered
              hoverable
              onRow={(row: Product) => ({
                className: isProductRowDisabled(row) ? 'opacity-50' : '',
              })}
            />

            <div className="mt-4 flex gap-2">
              <button
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                disabled={!selectedRows.length}
                onClick={() =>
                  alert(`Processing ${selectedRows.length} selected products`)
                }
              >
                Process Selected ({selectedRows.length})
              </button>
              <button
                className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
                onClick={() => handleProductSelectionChange([], [])}
              >
                Clear Selection
              </button>
            </div>
          </div>

          {/* Fixed Columns Table Example */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              3. Fixed Columns with Horizontal Scrolling
            </h3>
            <p className="text-gray-600 mb-4">
              Financial transactions table with fixed columns and horizontal
              scrolling. Date and Description are pinned to the left, Amount and
              Balance to the right.
            </p>

            <div className="mb-4 p-4 bg-yellow-50 rounded-lg">
              <p className="text-sm text-yellow-800">
                <strong>💡 Tip:</strong> Try scrolling horizontally to see the
                fixed column behavior in action!
              </p>
            </div>

            <Table
              data={transactionData}
              columns={transactionColumns}
              scroll={{ x: 1600 }}
              pagination={{
                page: 1,
                pageSize: 3,
                total: transactionData.length,
                showSizeChanger: true,
                showTotal: true,
              }}
              bordered
              hoverable
              size="small"
            />
          </div>

          {/* Advanced Table Example */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              4. Advanced Features Showcase
            </h3>
            <p className="text-gray-600 mb-4">
              Employee management table demonstrating all advanced features:
              multi-column sorting, complex cell rendering, fixed columns,
              selection with business rules, and real-time statistics.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold text-blue-900">
                  Selected Employees
                </h4>
                <p className="text-2xl font-bold text-blue-700">
                  {employeeSelectedRows.length}
                </p>
              </div>

              <div className="p-4 bg-green-50 rounded-lg">
                <h4 className="font-semibold text-green-900">Total Salary</h4>
                <p className="text-2xl font-bold text-green-700">
                  $
                  {employeeSelectedRows
                    .reduce((sum, emp) => sum + emp.salary, 0)
                    .toLocaleString()}
                </p>
              </div>

              <div className="p-4 bg-purple-50 rounded-lg">
                <h4 className="font-semibold text-purple-900">
                  Avg Performance
                </h4>
                <p className="text-2xl font-bold text-purple-700">
                  {employeeSelectedRows.length
                    ? (
                        employeeSelectedRows.reduce(
                          (sum, emp) => sum + emp.performance,
                          0
                        ) / employeeSelectedRows.length
                      ).toFixed(1)
                    : '0.0'}
                </p>
              </div>
            </div>

            <div className="mb-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex flex-wrap gap-2 mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Quick Actions:
                </span>
                <button
                  className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 disabled:opacity-50"
                  disabled={!employeeSelectedRows.length}
                  onClick={() =>
                    alert(`Promoting ${employeeSelectedRows.length} employees`)
                  }
                >
                  Promote Selected
                </button>
                <button
                  className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:opacity-50"
                  disabled={!employeeSelectedRows.length}
                  onClick={() =>
                    alert(
                      `Sending performance review to ${employeeSelectedRows.length} employees`
                    )
                  }
                >
                  Send Review
                </button>
                <button
                  className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700"
                  onClick={() => handleEmployeeSelectionChange([], [])}
                >
                  Clear Selection
                </button>
              </div>

              <When condition={Boolean(employeeSelectedRows.length)}>
                <div className="text-sm text-gray-600">
                  <strong>Selected:</strong>{' '}
                  {employeeSelectedRows
                    .map((emp) => `${emp.firstName} ${emp.lastName}`)
                    .join(', ')}
                </div>
              </When>
            </div>

            <Table
              data={employeeData.filter((emp) => emp.status === 'active')}
              columns={employeeColumns}
              selection={{
                type: 'multiple',
                selectedRowKeys: employeeSelectedRowKeys,
                onSelectionChange: handleEmployeeSelectionChange,
                getRowKey: (row: Employee) => row.id,
                disabled: isEmployeeRowDisabled,
              }}
              pagination={{
                page: 1,
                pageSize: 4,
                total: employeeData.filter((emp) => emp.status === 'active')
                  .length,
                showSizeChanger: true,
                showQuickJumper: false,
                showTotal: true,
                pageSizeOptions: [4, 6, 10],
              }}
              sorting={{
                multiple: true,
                defaultSort: [{ key: 'performance', direction: 'desc' }],
              }}
              scroll={{ x: 1400, y: 350 }}
              bordered
              hoverable
              size="small"
              onRow={(row: Employee) => ({
                onDoubleClick: () =>
                  alert(`Viewing details for ${row.firstName} ${row.lastName}`),
                className: 'cursor-pointer',
              })}
            />

            <div className="mt-4 text-sm text-gray-600 bg-gray-50 p-3 rounded">
              <p>
                <strong>🚀 Features demonstrated:</strong>
              </p>
              <ul className="list-disc list-inside mt-1 space-y-1">
                <li>
                  Multi-column sorting (hold Shift while clicking column
                  headers)
                </li>
                <li>Fixed columns (Name on left, Status on right)</li>
                <li>
                  Custom cell rendering with complex components (skills,
                  performance ratings)
                </li>
                <li>
                  Row selection with business logic (only active employees)
                </li>
                <li>Pagination with size options</li>
                <li>Horizontal and vertical scrolling</li>
                <li>Row double-click events</li>
                <li>Real-time statistics based on selection</li>
                <li>Responsive design and accessibility features</li>
              </ul>
            </div>
          </div>

          {/* Technical Summary */}
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              ✨ Technical Implementation Highlights
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">
                  🏗️ Architecture
                </h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Headless design with full styling control</li>
                  <li>• SOLID principles implementation</li>
                  <li>• Composable API with sub-components</li>
                  <li>• Context-based state management</li>
                  <li>• Custom hooks for business logic</li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 mb-2">
                  ⚡ Performance
                </h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• React.memo and useMemo optimizations</li>
                  <li>• Efficient sorting and filtering algorithms</li>
                  <li>• Minimal re-renders with proper dependencies</li>
                  <li>• Tree-shaking support for bundle optimization</li>
                  <li>• Virtualization ready for large datasets</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Example catalogs removed since deep imports are not exported by vizonomy-ui */}
      </div>
    </div>
  );
}
