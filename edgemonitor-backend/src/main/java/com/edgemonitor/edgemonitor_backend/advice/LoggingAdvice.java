package com.edgemonitor.edgemonitor_backend.advice;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import com.fasterxml.jackson.databind.ObjectMapper;

@Aspect
@Component
public class LoggingAdvice {

	Logger log =  LoggerFactory.getLogger(LoggingAdvice.class);
	
	@Pointcut("execution(* com.edgemonitor.edgemonitor_backend.*.*.*(..))")
	public void myPointcut() {}
	
	@Around("myPointcut()")
	public Object applicationLogger(ProceedingJoinPoint pjp) throws Throwable {
//		ObjectMapper mapper = new ObjectMapper();
		String className = pjp.getTarget().getClass().toString();
		String methodName = pjp.getSignature().getName();
//		Object[] args = pjp.getArgs();
		log.info("method invoked "+ className + " : " + methodName+"()");
		Object obj = pjp.proceed();
		return obj;
	}
	
	
    @AfterThrowing(pointcut = "execution(* com.edgemonitor.edgemonitor_backend.*.*.*(..))", throwing = "ex")
    public void logAfterThrowing(JoinPoint joinPoint, Throwable ex) {
        String methodName = joinPoint.getSignature().toShortString();
        log.error("❌ Exception in method: {}", methodName, ex);
    }
}
