/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AssetQualityLevel } from './AssetQualityLevel';
import type { AssetViewAngle } from './AssetViewAngle';
export type CharacterImageRead = {
    /**
     * 图片行 ID
     */
    id: number;
    /**
     * 精度等级
     */
    quality_level?: AssetQualityLevel;
    /**
     * 视角
     */
    view_angle?: AssetViewAngle;
    /**
     * 关联的 FileItem ID（可空，支持先创建槽位后填充）
     */
    file_id?: (string | null);
    /**
     * 宽(px)
     */
    width?: (number | null);
    /**
     * 高(px)
     */
    height?: (number | null);
    /**
     * 格式
     */
    format?: string;
    character_id: string;
};

