export interface MetricsModel {
  timestamp: string;
  total_system_runtime: string;
  cpu_percent: number;
  ram: { total_mb: number; used_mb: number; percent: number };
  disk: { total_gb: number; used_gb: number; percent: number };
  gpu: any;
  temperature_celsius: number;
}