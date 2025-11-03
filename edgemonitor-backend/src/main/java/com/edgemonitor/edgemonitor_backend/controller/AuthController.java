package com.edgemonitor.edgemonitor_backend.controller;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.edgemonitor.edgemonitor_backend.dto.AuthenticationResponse;
import com.edgemonitor.edgemonitor_backend.dto.LoginRequest;
import com.edgemonitor.edgemonitor_backend.dto.SignupRequest;
import com.edgemonitor.edgemonitor_backend.dto.UserDto;
import com.edgemonitor.edgemonitor_backend.entity.User;
import com.edgemonitor.edgemonitor_backend.services.auth.AuthService;
import com.edgemonitor.edgemonitor_backend.utils.JWTUtil;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
		
		@Autowired
		private final AuthService authService;
		@Autowired
	    private JWTUtil jwtUtil;
		
		public AuthController(AuthService authService) {
			this.authService = authService;
		}

		@PostMapping("/signup")
		public ResponseEntity<?> signupUser(@RequestBody SignupRequest signupRequest){
			UserDto createdUserDto = authService.createUser(signupRequest);
			if(createdUserDto == null) {
				return new ResponseEntity<>("User not Registered", HttpStatus.BAD_REQUEST);
			}
			return new ResponseEntity<>(createdUserDto, HttpStatus.CREATED);
		}
		
		@GetMapping("/hello")
		public String getMap(){
			return "API up and Running";
		}
		
	    @PostMapping("/login")
	    public Map<String, String> login(@RequestBody LoginRequest loginRequestUser) {
	    	Optional<User> logedInUser = authService.loginUser(loginRequestUser);
	    	Map<String, String> resp = new HashMap<>();
	    	AuthenticationResponse authenticationResponse = new AuthenticationResponse();
	        if (logedInUser.isPresent() && logedInUser.get().getPassword().equals(loginRequestUser.getPassword())) {
	            String token = jwtUtil.generateToken(logedInUser.get().getUsername());
	            authenticationResponse.setJwt(token);
	            authenticationResponse.setUserId(logedInUser.get().getId());
	            resp.put("jwt", token);
	            resp.put("userId", logedInUser.get().getId().toString());
	        } else {
	            resp.put("error", "Invalid credentials");
	        }
	        return resp;
	    }
		
}
