/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApiResponse_ImportFromExtractionResponse_ } from '../models/ApiResponse_ImportFromExtractionResponse_';
import type { ImportFromExtractionRequest } from '../models/ImportFromExtractionRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class StudioImportService {
    /**
     * 从信息提取草稿导入 Studio 数据
     * 接收 StudioScriptExtractionDraft（name-based，不含 id），由接口生成 ID 并在一个事务内创建：Scene/Prop/Costume/Character/Shot/ShotDetail/Links/ShotDialogLine。默认不覆盖：遇到同项目同名或同章节镜头 index 冲突即回滚报错并提示重复。设置 force_overwrite=true 时，将覆盖更新已存在数据并重建相关 links/对白。
     * @returns ApiResponse_ImportFromExtractionResponse_ Successful Response
     * @throws ApiError
     */
    public static importFromExtractionApiV1StudioImportFromExtractionPost({
        requestBody,
    }: {
        requestBody: ImportFromExtractionRequest,
    }): CancelablePromise<ApiResponse_ImportFromExtractionResponse_> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/studio/import-from-extraction',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
