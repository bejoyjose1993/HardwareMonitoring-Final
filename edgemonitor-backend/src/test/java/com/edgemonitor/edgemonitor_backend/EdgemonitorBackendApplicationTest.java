package com.edgemonitor.edgemonitor_backend;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import com.edgemonitor.edgemonitor_backend.dto.LoginRequest;
import com.edgemonitor.edgemonitor_backend.entity.User;
import com.edgemonitor.edgemonitor_backend.repository.UserRepository;
import com.edgemonitor.edgemonitor_backend.services.auth.AuthServiceImp;


class EdgemonitorBackendApplicationTest {

    @Mock
    private UserRepository userRepo;

    @InjectMocks
    private AuthServiceImp authService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
	@Test
    void loginUser_WhenUserExists_ShouldReturnUser() {
        String email = "mytestemail@gmail.com";
        LoginRequest loginRequest = new LoginRequest();
        loginRequest.setEmail(email);

        User mockUser = new User();
        mockUser.setEmail(email);

        when(userRepo.findFirstByEmail(email)).thenReturn(Optional.of(mockUser));

        Optional<User> result = authService.loginUser(loginRequest);

        assertTrue(result.isPresent());
        assertEquals(email, result.get().getEmail());
        verify(userRepo, times(1)).findFirstByEmail(email);
    }
	
	
	 @Test
	 void loginUser_WhenUserDoesNotExist_ShouldReturnEmptyOptional() {

		 String email = "myunknownemail@gmail.com";
		 LoginRequest loginRequest = new LoginRequest();
	     loginRequest.setEmail(email);

	     when(userRepo.findFirstByEmail(email)).thenReturn(Optional.empty());

	     Optional<User> result = authService.loginUser(loginRequest);

	     assertFalse(result.isPresent());
	     verify(userRepo, times(1)).findFirstByEmail(email);
	 }	
	

}
