package com.edgemonitor.edgemonitor_backend.utils;

import java.security.Key;
import java.util.*;
import javax.crypto.spec.SecretKeySpec;
import org.springframework.stereotype.Component;

import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

@Component
public class JWTUtil {
	 private final String SECRET = "2D4A614E645267556B58703273357638792F423F4428472B4B6250655368566D";
	    private final long EXPIRATION = 1000 * 60 * 10; // 10 minutes

	    private Key getSigningKey() {
	        byte[] keyBytes = SECRET.getBytes();
	        return new SecretKeySpec(keyBytes, SignatureAlgorithm.HS256.getJcaName());
	    }
	    
	    public String generateToken(String username) {
	        return Jwts.builder()
	            .setSubject(username)
	            .setIssuedAt(new Date(System.currentTimeMillis()))
	            .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION))
	            .signWith(getSigningKey(), SignatureAlgorithm.HS256)
	            .compact();
	    }

	    public String extractUsername(String token) {
	        try {
	            return Jwts.parserBuilder()
	                .setSigningKey(getSigningKey())
	                .build()
	                .parseClaimsJws(token)
	                .getBody()
	                .getSubject();
	        } catch (JwtException e) {
	            // Log and handle invalid/expired token
	            return null;
	        }
	    }
}
