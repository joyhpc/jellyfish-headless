/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AssetQualityLevel } from './AssetQualityLevel';
import type { AssetViewAngle } from './AssetViewAngle';
export type ActorImageRead = {
    id: number;
    actor_id: string;
    quality_level?: AssetQualityLevel;
    view_angle?: AssetViewAngle;
    file_id?: (string | null);
    width?: (number | null);
    height?: (number | null);
    format?: string;
};

