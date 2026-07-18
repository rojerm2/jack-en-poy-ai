package com.orcific.jackenpoyai.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class ApiResponse<T> {
    private boolean success;
    private String message;
    private T data;

    public static <T> ApiResponse<T> success(T data){
        return new ApiResponse<>(
                true,
                "Game done",
                data
        );
    }

    public static <T> ApiResponse<T> error(String message){
        return new ApiResponse<>(
                false,
                message,
                null
        );
    }
}
