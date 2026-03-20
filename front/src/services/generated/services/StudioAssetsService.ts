/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApiResponse_CostumeImageRead_ } from '../models/ApiResponse_CostumeImageRead_';
import type { ApiResponse_CostumeRead_ } from '../models/ApiResponse_CostumeRead_';
import type { ApiResponse_NoneType_ } from '../models/ApiResponse_NoneType_';
import type { ApiResponse_PaginatedData_CostumeImageRead__ } from '../models/ApiResponse_PaginatedData_CostumeImageRead__';
import type { ApiResponse_PaginatedData_CostumeRead__ } from '../models/ApiResponse_PaginatedData_CostumeRead__';
import type { ApiResponse_PaginatedData_PropImageRead__ } from '../models/ApiResponse_PaginatedData_PropImageRead__';
import type { ApiResponse_PaginatedData_PropRead__ } from '../models/ApiResponse_PaginatedData_PropRead__';
import type { ApiResponse_PaginatedData_SceneImageRead__ } from '../models/ApiResponse_PaginatedData_SceneImageRead__';
import type { ApiResponse_PaginatedData_SceneRead__ } from '../models/ApiResponse_PaginatedData_SceneRead__';
import type { ApiResponse_PropImageRead_ } from '../models/ApiResponse_PropImageRead_';
import type { ApiResponse_PropRead_ } from '../models/ApiResponse_PropRead_';
import type { ApiResponse_SceneImageRead_ } from '../models/ApiResponse_SceneImageRead_';
import type { ApiResponse_SceneRead_ } from '../models/ApiResponse_SceneRead_';
import type { AssetCreate } from '../models/AssetCreate';
import type { AssetImageCreate } from '../models/AssetImageCreate';
import type { AssetImageUpdate } from '../models/AssetImageUpdate';
import type { AssetUpdate } from '../models/AssetUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class StudioAssetsService {
    /**
     * 场景列表（分页）
     * @returns ApiResponse_PaginatedData_SceneRead__ Successful Response
     * @throws ApiError
     */
    public static listScenesApiV1StudioAssetsScenesGet({
        q,
        order,
        isDesc = false,
        page = 1,
        pageSize = 10,
    }: {
        /**
         * 关键字，过滤 name/description
         */
        q?: (string | null),
        order?: (string | null),
        isDesc?: boolean,
        page?: number,
        pageSize?: number,
    }): CancelablePromise<ApiResponse_PaginatedData_SceneRead__> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/studio/assets/scenes',
            query: {
                'q': q,
                'order': order,
                'is_desc': isDesc,
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 创建场景
     * @returns ApiResponse_SceneRead_ Successful Response
     * @throws ApiError
     */
    public static createSceneApiV1StudioAssetsScenesPost({
        requestBody,
    }: {
        requestBody: AssetCreate,
    }): CancelablePromise<ApiResponse_SceneRead_> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/studio/assets/scenes',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 获取场景
     * @returns ApiResponse_SceneRead_ Successful Response
     * @throws ApiError
     */
    public static getSceneApiV1StudioAssetsScenesSceneIdGet({
        sceneId,
    }: {
        sceneId: string,
    }): CancelablePromise<ApiResponse_SceneRead_> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/studio/assets/scenes/{scene_id}',
            path: {
                'scene_id': sceneId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 更新场景
     * @returns ApiResponse_SceneRead_ Successful Response
     * @throws ApiError
     */
    public static updateSceneApiV1StudioAssetsScenesSceneIdPatch({
        sceneId,
        requestBody,
    }: {
        sceneId: string,
        requestBody: AssetUpdate,
    }): CancelablePromise<ApiResponse_SceneRead_> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/studio/assets/scenes/{scene_id}',
            path: {
                'scene_id': sceneId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 删除场景
     * @returns ApiResponse_NoneType_ Successful Response
     * @throws ApiError
     */
    public static deleteSceneApiV1StudioAssetsScenesSceneIdDelete({
        sceneId,
    }: {
        sceneId: string,
    }): CancelablePromise<ApiResponse_NoneType_> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/studio/assets/scenes/{scene_id}',
            path: {
                'scene_id': sceneId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 场景图片列表（分页）
     * @returns ApiResponse_PaginatedData_SceneImageRead__ Successful Response
     * @throws ApiError
     */
    public static listSceneImagesApiV1StudioAssetsScenesSceneIdImagesGet({
        sceneId,
        order,
        isDesc = false,
        page = 1,
        pageSize = 10,
    }: {
        sceneId: string,
        order?: (string | null),
        isDesc?: boolean,
        page?: number,
        pageSize?: number,
    }): CancelablePromise<ApiResponse_PaginatedData_SceneImageRead__> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/studio/assets/scenes/{scene_id}/images',
            path: {
                'scene_id': sceneId,
            },
            query: {
                'order': order,
                'is_desc': isDesc,
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 创建场景图片
     * @returns ApiResponse_SceneImageRead_ Successful Response
     * @throws ApiError
     */
    public static createSceneImageApiV1StudioAssetsScenesSceneIdImagesPost({
        sceneId,
        requestBody,
    }: {
        sceneId: string,
        requestBody: AssetImageCreate,
    }): CancelablePromise<ApiResponse_SceneImageRead_> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/studio/assets/scenes/{scene_id}/images',
            path: {
                'scene_id': sceneId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 更新场景图片
     * @returns ApiResponse_SceneImageRead_ Successful Response
     * @throws ApiError
     */
    public static updateSceneImageApiV1StudioAssetsScenesSceneIdImagesImageIdPatch({
        sceneId,
        imageId,
        requestBody,
    }: {
        sceneId: string,
        imageId: number,
        requestBody: AssetImageUpdate,
    }): CancelablePromise<ApiResponse_SceneImageRead_> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/studio/assets/scenes/{scene_id}/images/{image_id}',
            path: {
                'scene_id': sceneId,
                'image_id': imageId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 删除场景图片
     * @returns ApiResponse_NoneType_ Successful Response
     * @throws ApiError
     */
    public static deleteSceneImageApiV1StudioAssetsScenesSceneIdImagesImageIdDelete({
        sceneId,
        imageId,
    }: {
        sceneId: string,
        imageId: number,
    }): CancelablePromise<ApiResponse_NoneType_> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/studio/assets/scenes/{scene_id}/images/{image_id}',
            path: {
                'scene_id': sceneId,
                'image_id': imageId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 道具列表（分页）
     * @returns ApiResponse_PaginatedData_PropRead__ Successful Response
     * @throws ApiError
     */
    public static listPropsApiV1StudioAssetsPropsGet({
        q,
        order,
        isDesc = false,
        page = 1,
        pageSize = 10,
    }: {
        /**
         * 关键字，过滤 name/description
         */
        q?: (string | null),
        order?: (string | null),
        isDesc?: boolean,
        page?: number,
        pageSize?: number,
    }): CancelablePromise<ApiResponse_PaginatedData_PropRead__> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/studio/assets/props',
            query: {
                'q': q,
                'order': order,
                'is_desc': isDesc,
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 创建道具
     * @returns ApiResponse_PropRead_ Successful Response
     * @throws ApiError
     */
    public static createPropApiV1StudioAssetsPropsPost({
        requestBody,
    }: {
        requestBody: AssetCreate,
    }): CancelablePromise<ApiResponse_PropRead_> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/studio/assets/props',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 获取道具
     * @returns ApiResponse_PropRead_ Successful Response
     * @throws ApiError
     */
    public static getPropApiV1StudioAssetsPropsPropIdGet({
        propId,
    }: {
        propId: string,
    }): CancelablePromise<ApiResponse_PropRead_> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/studio/assets/props/{prop_id}',
            path: {
                'prop_id': propId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 更新道具
     * @returns ApiResponse_PropRead_ Successful Response
     * @throws ApiError
     */
    public static updatePropApiV1StudioAssetsPropsPropIdPatch({
        propId,
        requestBody,
    }: {
        propId: string,
        requestBody: AssetUpdate,
    }): CancelablePromise<ApiResponse_PropRead_> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/studio/assets/props/{prop_id}',
            path: {
                'prop_id': propId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 删除道具
     * @returns ApiResponse_NoneType_ Successful Response
     * @throws ApiError
     */
    public static deletePropApiV1StudioAssetsPropsPropIdDelete({
        propId,
    }: {
        propId: string,
    }): CancelablePromise<ApiResponse_NoneType_> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/studio/assets/props/{prop_id}',
            path: {
                'prop_id': propId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 道具图片列表（分页）
     * @returns ApiResponse_PaginatedData_PropImageRead__ Successful Response
     * @throws ApiError
     */
    public static listPropImagesApiV1StudioAssetsPropsPropIdImagesGet({
        propId,
        order,
        isDesc = false,
        page = 1,
        pageSize = 10,
    }: {
        propId: string,
        order?: (string | null),
        isDesc?: boolean,
        page?: number,
        pageSize?: number,
    }): CancelablePromise<ApiResponse_PaginatedData_PropImageRead__> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/studio/assets/props/{prop_id}/images',
            path: {
                'prop_id': propId,
            },
            query: {
                'order': order,
                'is_desc': isDesc,
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 创建道具图片
     * @returns ApiResponse_PropImageRead_ Successful Response
     * @throws ApiError
     */
    public static createPropImageApiV1StudioAssetsPropsPropIdImagesPost({
        propId,
        requestBody,
    }: {
        propId: string,
        requestBody: AssetImageCreate,
    }): CancelablePromise<ApiResponse_PropImageRead_> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/studio/assets/props/{prop_id}/images',
            path: {
                'prop_id': propId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 更新道具图片
     * @returns ApiResponse_PropImageRead_ Successful Response
     * @throws ApiError
     */
    public static updatePropImageApiV1StudioAssetsPropsPropIdImagesImageIdPatch({
        propId,
        imageId,
        requestBody,
    }: {
        propId: string,
        imageId: number,
        requestBody: AssetImageUpdate,
    }): CancelablePromise<ApiResponse_PropImageRead_> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/studio/assets/props/{prop_id}/images/{image_id}',
            path: {
                'prop_id': propId,
                'image_id': imageId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 删除道具图片
     * @returns ApiResponse_NoneType_ Successful Response
     * @throws ApiError
     */
    public static deletePropImageApiV1StudioAssetsPropsPropIdImagesImageIdDelete({
        propId,
        imageId,
    }: {
        propId: string,
        imageId: number,
    }): CancelablePromise<ApiResponse_NoneType_> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/studio/assets/props/{prop_id}/images/{image_id}',
            path: {
                'prop_id': propId,
                'image_id': imageId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 服装列表（分页）
     * @returns ApiResponse_PaginatedData_CostumeRead__ Successful Response
     * @throws ApiError
     */
    public static listCostumesApiV1StudioAssetsCostumesGet({
        q,
        order,
        isDesc = false,
        page = 1,
        pageSize = 10,
    }: {
        /**
         * 关键字，过滤 name/description
         */
        q?: (string | null),
        order?: (string | null),
        isDesc?: boolean,
        page?: number,
        pageSize?: number,
    }): CancelablePromise<ApiResponse_PaginatedData_CostumeRead__> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/studio/assets/costumes',
            query: {
                'q': q,
                'order': order,
                'is_desc': isDesc,
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 创建服装
     * @returns ApiResponse_CostumeRead_ Successful Response
     * @throws ApiError
     */
    public static createCostumeApiV1StudioAssetsCostumesPost({
        requestBody,
    }: {
        requestBody: AssetCreate,
    }): CancelablePromise<ApiResponse_CostumeRead_> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/studio/assets/costumes',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 获取服装
     * @returns ApiResponse_CostumeRead_ Successful Response
     * @throws ApiError
     */
    public static getCostumeApiV1StudioAssetsCostumesCostumeIdGet({
        costumeId,
    }: {
        costumeId: string,
    }): CancelablePromise<ApiResponse_CostumeRead_> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/studio/assets/costumes/{costume_id}',
            path: {
                'costume_id': costumeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 更新服装
     * @returns ApiResponse_CostumeRead_ Successful Response
     * @throws ApiError
     */
    public static updateCostumeApiV1StudioAssetsCostumesCostumeIdPatch({
        costumeId,
        requestBody,
    }: {
        costumeId: string,
        requestBody: AssetUpdate,
    }): CancelablePromise<ApiResponse_CostumeRead_> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/studio/assets/costumes/{costume_id}',
            path: {
                'costume_id': costumeId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 删除服装
     * @returns ApiResponse_NoneType_ Successful Response
     * @throws ApiError
     */
    public static deleteCostumeApiV1StudioAssetsCostumesCostumeIdDelete({
        costumeId,
    }: {
        costumeId: string,
    }): CancelablePromise<ApiResponse_NoneType_> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/studio/assets/costumes/{costume_id}',
            path: {
                'costume_id': costumeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 服装图片列表（分页）
     * @returns ApiResponse_PaginatedData_CostumeImageRead__ Successful Response
     * @throws ApiError
     */
    public static listCostumeImagesApiV1StudioAssetsCostumesCostumeIdImagesGet({
        costumeId,
        order,
        isDesc = false,
        page = 1,
        pageSize = 10,
    }: {
        costumeId: string,
        order?: (string | null),
        isDesc?: boolean,
        page?: number,
        pageSize?: number,
    }): CancelablePromise<ApiResponse_PaginatedData_CostumeImageRead__> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/studio/assets/costumes/{costume_id}/images',
            path: {
                'costume_id': costumeId,
            },
            query: {
                'order': order,
                'is_desc': isDesc,
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 创建服装图片
     * @returns ApiResponse_CostumeImageRead_ Successful Response
     * @throws ApiError
     */
    public static createCostumeImageApiV1StudioAssetsCostumesCostumeIdImagesPost({
        costumeId,
        requestBody,
    }: {
        costumeId: string,
        requestBody: AssetImageCreate,
    }): CancelablePromise<ApiResponse_CostumeImageRead_> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/studio/assets/costumes/{costume_id}/images',
            path: {
                'costume_id': costumeId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 更新服装图片
     * @returns ApiResponse_CostumeImageRead_ Successful Response
     * @throws ApiError
     */
    public static updateCostumeImageApiV1StudioAssetsCostumesCostumeIdImagesImageIdPatch({
        costumeId,
        imageId,
        requestBody,
    }: {
        costumeId: string,
        imageId: number,
        requestBody: AssetImageUpdate,
    }): CancelablePromise<ApiResponse_CostumeImageRead_> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/studio/assets/costumes/{costume_id}/images/{image_id}',
            path: {
                'costume_id': costumeId,
                'image_id': imageId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * 删除服装图片
     * @returns ApiResponse_NoneType_ Successful Response
     * @throws ApiError
     */
    public static deleteCostumeImageApiV1StudioAssetsCostumesCostumeIdImagesImageIdDelete({
        costumeId,
        imageId,
    }: {
        costumeId: string,
        imageId: number,
    }): CancelablePromise<ApiResponse_NoneType_> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/studio/assets/costumes/{costume_id}/images/{image_id}',
            path: {
                'costume_id': costumeId,
                'image_id': imageId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
